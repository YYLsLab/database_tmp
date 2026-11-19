"""Generate a README and an energy plot for each charge-state series."""

import json
from math import ceil, exp, floor, pi, sqrt
from pathlib import Path
from statistics import mean, pvariance

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


FIELDS = ("TransitionLevel", "Er12", "Er21")
SERIES = {"VO_HfO2_plus1_0": "(+1/0)", "VO_HfO2_0_minus1": "(0/-1)"}
ROOT = Path(__file__).resolve().parents[1]


def summarize(directory, charge_pair):
    records = []
    for sample in sorted(directory.iterdir()):
        if sample.is_dir() and len(sample.name) == 3 and sample.name.isdecimal():
            path = sample / f"{directory.name}.json"
            record = json.loads(path.read_text(encoding="utf-8"))
            records.append((sample.name, tuple(record[field] for field in FIELDS)))

    if not records or records[0][0] != "001":
        raise ValueError(f"Missing baseline record 001 in {directory}")

    columns = list(zip(*(values for _, values in records)))
    averages = [mean(values) for values in columns]
    variances = [pvariance(values) for values in columns]

    figure_dir = directory / "figs"
    figure_dir.mkdir(exist_ok=True)
    figure, axes = plt.subplots(1, 3, figsize=(12, 3.8), layout="constrained")
    bin_width = 0.1
    for axis, field, values, average, variance in zip(axes, FIELDS, columns, averages, variances):
        sigma = sqrt(variance)
        lower = floor(min(min(values), average - 3 * sigma) / bin_width)
        upper = max(lower + 1, ceil(max(max(values), average + 3 * sigma) / bin_width))
        edges = [index * bin_width for index in range(lower, upper + 1)]
        axis.set_facecolor("#eef2f7")
        axis.hist(values, bins=edges, color="#fa7a77", edgecolor="white")
        if sigma > 0:
            xs = [edges[0] + (edges[-1] - edges[0]) * index / 299 for index in range(300)]
            amplitude = len(values) * bin_width / (sigma * sqrt(2 * pi))
            ys = [amplitude * exp(-0.5 * ((x - average) / sigma) ** 2) for x in xs]
            axis.plot(xs, ys, color="#394658", linewidth=2)

        axis.set_xlabel(f"{field} (eV)")
        axis.set_ylabel("Counts")
        axis.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
        axis.set_ylim(bottom=0)
    figure.savefig(figure_dir / "energy_statistics.png", dpi=180)
    plt.close(figure)

    lines = [
        f"# VO@HfO2 {charge_pair}",
        "",
        f"统计目录中的 {len(records)} 条记录。001 来自原始 DFT 计算，其余记录为随机生成的测试数据。",
        "统计直接使用 JSON 中的三个能量字段。转变能级相对于 PBE VBM。方差为总体方差，分母为记录数 N。",
        "",
        "## 汇总统计",
        "",
        "| 参数 | 平均值（eV） | 总体方差（eV²） |",
        "|---|---:|---:|",
    ]
    for field, average, variance in zip(FIELDS, averages, variances):
        lines.append(f"| {field} | {average:.6f} | {variance:.6f} |")

    lines.extend([
        "",
        "## 能量分布",
        "",
        f"柱高为每个 {bin_width:g} eV 区间内的记录数。深色曲线为高斯拟合，使用表中的平均值与总体方差，并按记录数和组距缩放到计数尺度。",
        "",
        "![各记录的转变能级及重组能](figs/energy_statistics.png)",
    ])

    lines.extend([
        "",
        "## 逐条数据（eV）",
        "",
        "| 编号 | TransitionLevel | Er12 | Er21 |",
        "|---|---:|---:|---:|",
    ])
    for label, values in records:
        numbers = " | ".join(f"{value:.6f}" for value in values)
        lines.append(f"| [{label}]({label}/{directory.name}.json) | {numbers} |")
    lines.append("")
    (directory / "README.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    for name, charge_pair in SERIES.items():
        summarize(ROOT / name, charge_pair)
