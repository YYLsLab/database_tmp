# Repository Guidelines

## Project Structure

This repository is starting from an empty Git history. As you add code, group related modules together and follow the directory conventions of the chosen language or framework. Put tests alongside the code they exercise or in a dedicated test directory, as the framework recommends. Keep fixtures with their tests and document any assets needed to run the project.

## Build and Development

When introducing the first runnable component, add a README with prerequisites, dependency installation, and the commands to build, run, and test it from a fresh checkout. Include any required configuration and use placeholders for credentials. Update the README whenever a change affects these steps.

## Coding Style and Naming

Follow the chosen language's standard naming and indentation conventions. Once the repository adopts a formatter or linter, use its checked-in configuration and document the commands contributors should run. Name files and functions for their purpose, and follow neighboring code when extending an existing module.

## Testing

Run the documented checks for each component you change. Add focused regression tests for bug fixes and tests for new behavior where practical. Follow the test runner's discovery conventions and name each test for the behavior it verifies. When introducing a test runner, document how to run the full suite and an individual test from the repository root.

## Commits and Pull Requests

Use short, imperative commit subjects such as `Document local setup`. Keep each commit focused on one change. In a pull request, describe the change and its purpose, list the checks you ran and their results, and link related issues when available. Include screenshots or recordings for visible interface changes.
