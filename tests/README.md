# Tests

All logical game-related and data-related tests are found here.

Their purpose is to test the inner functionalities of the game and the existence of files used by it.

Unit tests are found under the `unit/` directory, integrated tests are found under the `integrated/` directory.

## Running a test

Install the required dependencies using (run in root dir):

```bash
pip install -e .[test_modules]
```

If you want, position yourself in the `tests` directory using:

```bash
cd tests
```

- To run all tests:

```bash
pytest .
```

- To run all tests of a certain type:

```bash
pytest [unit|integrated] # Either unit or integrated
```

- To run tests in a specific module:

```bash
pytest unit/test_core.py  # Example
```

- To run a specific test of a module:

```bash
pytest unit/test_core.py::test_window_creation  # Example
```

> If you're in the root directory, make sure to add `tests/` to the path argument (e.g. `pytest tests/test_assets.py`) or replace it entirely if the path is `.` (like the third command above).

## Information

Developed by [SammygoodTunes](https://github.com/SammygoodTunes)

Tested on Debian 12 and Windows 10

Libraries used: PyTest 8.1.1
