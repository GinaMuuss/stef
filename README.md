# STEF: Submission TEst Framework

STEF is a lightweight testing framework designed to automatically test student program submissions that interact over stdin/stdout.
It provides runners for executing programs locally in a shell or inside Docker containers and utilities for composing tests.

## Key goals
- Provide deterministic, repeatable testing of console-based student submissions.
- Make it easy to run many test cases automatically and capture program output for grading.
- Support multiple execution environments (local, shell wrapper, Docker).

## Project layout
- `stef/` : Core package code.
	- `base.py` : Core base classes and interfaces for runners and test abstractions.
	- `runner.py` : Main runner implementation used to orchestrate test execution.
	- `bashrunner.py` : Runner that executes commands through a shell.
	- `dockerrunner.py` : Runner that executes submissions inside Docker containers for isolation.
	- `logger.py` : Logging helpers used across the package.
	- `scripts/runtests.py` : CLI helper script to run a suite of tests from the command line.

## Installation

Install from PyPI or install locally for development:

#### From local checkout (editable): `pip install -e .`

#### Or from pypi: `pip install stef`

## Criteria for program to test

1. There has to an executable file `run.sh` which calls the code.
2. If the program needs compilation, there should be a `Makefile`
3. The program itself can output arbitrary outputs but lines that contains solutions need to start with the string "SOLUTION:"
4. The first parameter that the programm should parse is the subcommand that shall invoked
   stef calls this a testgroup internally.
   There needs to be at least one.

## Quickstart

* Prepare a test input and expected output. STEF feeds the program's via stdin and captures output from stdout. Test cases are plain Python code.

A `test.py` file which could look like this:

```python
from stef.base import TestBase, TestType

class Test(TestBase):
    def __init__(self):
        super().__init__("example", TestType.shown)
        self.testgroups = [
            {"name": "square", "function": self.test_square},
            {"name": "cube", "function": self.test_cube}
        ]

    def test_square(self):
        self.test(["square", "5"], [], [["25.0"]], 1)
        self.test(["square", "11"], [], [["121.0"]], 1)

    def test_cube(self):
        self.test(["cube", "3"], [], [["27.0"]], 1)
        self.test(["cube", "20"], [], [["8000.0"]], 1)
```
By default all testgroups are run, but the `--testgroups` parameter can be to only run the selected (comma separated) testgroups.

* Run the tests using the provided CLI script (command `stef_runtests`)
The first parameter is directory with the code to test and the second parameter is the directory to load the tests from.

```bash
stef_runtests . .
```
Additional paramters along their documentation can be viewed with
```
stef_runtests --help
```
