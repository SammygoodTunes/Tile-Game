# Tests

All logical game-related and data-related tests are found here.

Their purpose is to test the inner functionalities of the game.

Each function of each component of the game will be called in alphabetical order.

## Running a test

> Pytest must be installed before running tests, see the README file (root dir).

If you haven't already, position yourself in the `tests` directory using:

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

## Information

Developed by [SammygoodTunes](https://github.com/SammygoodTunes)

Tested on Debian 12 and Windows 10

Libraries used: PyTest 8.1.1
