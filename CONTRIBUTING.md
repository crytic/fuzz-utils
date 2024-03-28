# Contributing to fuzz-utils

First, thanks for your interest in contributing to `fuzz-utils`! We welcome and appreciate all contributions, including bug reports, feature suggestions, tutorials/blog posts, and code improvements.

If you're unsure where to start, we recommend our [`good first issue`](https://github.com/crytic/fuzz-utils/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) and [`help wanted`](https://github.com/crytic/fuzz-utils/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22) issue labels.

## Bug reports and feature suggestions

Bug reports and feature suggestions can be submitted to our issue tracker. For bug reports, attaching the contract and the call sequence that caused the bug will help us in debugging and resolving the issue quickly. If you find a security vulnerability, do not open an issue; email opensource@trailofbits.com instead.

## Questions

Questions can be submitted to the "Discussions" page, and you may also join our [chat room](https://empireslacking.herokuapp.com/) (in the #ethereum channel).

## Code

`fuzz-utils` uses the pull request contribution model. Please make an account on Github, fork this repo, and submit code contributions via pull request. For more documentation, look [here](https://guides.github.com/activities/forking/).

Some pull request guidelines:


- Minimize irrelevant changes (formatting, whitespace, etc) to code that would otherwise not be touched by this patch. Save formatting or style corrections for a separate pull request that does not make any semantic changes.
- When possible, large changes should be split up into smaller focused pull requests.
- Fill out the pull request description with a summary of what your patch does, key changes that have been made, and any further points of discussion, if applicable.
- Title your pull request with a brief description of what it's changing. "Fixes #123" is a good comment to add to the description, but makes for an unclear title on its own.

## Directory Structure

Below is a rough outline of fuzz-utils's design:

```text
.
├── generate # Classes related to the `generate` command
|   └── fuzzers # Supported fuzzer classes
├── parsing # Contains the main parser logic
|   └── commands # Flags and execution logic per supported subparser
├── template # Classes related to the `template` command
├── templates # Common templates such as the default config and templates for test and harness generation
├── utils # Utility functions
├── main.py # Main entry point
└── ...
```

## Development Environment

`fuzz-utils` currently runs requires at least Python3.10 so make sure you have a sufficiently up-to-date installation by running `python --version`. We recommend [pyenv](https://github.com/pyenv/pyenv) to manage python versions.

To start working on modifications to fuzz-utils locally, run:
```bash
git clone https://github.com/crytic/fuzz-utils
cd fuzz-utils
make dev
```
This will create a virtual environment, ./env/, in the root of the repository and install dependencies.

To run commands using your development version of `fuzz-utils`, run:
```bash
source ./env/bin/activate
```

### Setting up IDE-based debugging
1. Configure your IDE to use `./env/bin/python` as the interpreter.
2. Use `fuzz-utils` as the entrypoint for the debugger.
3. Pycharm specific: Set the environment working directory to `./env/bin/`

To run the unit tests, you need to clone this repository and run `make test`. Run a specific test with `make test TESTS=$test_name`. The names of tests can be obtained with `pytest tests --collect-only`.

### Linters

Several linters and security checkers are run on the PRs.

To run them locally in the root dir of the repository:

- `make lint`

> Note, this only validates but does not modify the code.

To automatically reformat the code:

- `make reformat`

We use pylint `2.13.4`, black `22.3.0`.