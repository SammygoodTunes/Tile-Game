# Tests

All logical game-related and data-related tests are found here.

Their purpose is to test the inner functionalities of the game and the existence of files used by it.

## Running a test

> Make sure to install all the dependencies before running the tests, see the README file (root dir).

If you want, position yourself in the `tests` directory using:

```bash
cd tests
```

- To run all tests:

```bash
pytest .
```

- To run tests in a specific module:

```bash
pytest test_assets.py # Example
```

- To run a specific test of a module:

```bash
pytest test_assets.py::test_assets_folder_exists # Example
```

> If you're in the root directory, make sure to add `tests/` to the path argument (e.g. `pytest tests/test_assets.py`) or replace it entirely if the path is `.` (like the first command above).

## Information

Developed by [SammygoodTunes](https://github.com/SammygoodTunes)

Tested on Debian 12 and Windows 10

Libraries used: PyTest 8.1.1
