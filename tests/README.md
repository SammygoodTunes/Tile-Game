# Tests

All logical game-related and data-related tests are found here.

Unit tests are found under the `unit/` directory, integrated tests are found under the `integrated/` directory.

## Running a test

In order to run any of the tests, the development dependencies are required.

If you installed the modules with the ```--only main``` flag, then you can install the missing ones without it like so:

```bash
poetry install
```

> The above part requires Poetry to be installed. Please refer to [this page](https://github.com/SammygoodTunes/Tile-Game?tab=readme-ov-file#setup)
> to know how to install it. If you wish to know more about this module, see [here](https://python-poetry.org/docs/) 
> for its official documentation and [here](https://python-poetry.org/docs/cli) for its official CLI documentation. 

You may position yourself in the `tests` directory using:

```bash
cd tests
```

- To run all tests in a directory:

```bash
pytest .
```

- To run all tests of a certain type:

```bash
pytest [unit|integrated]  # Either unit or integrated
```

- To run all tests of a specific module:

```bash
pytest unit/core/test_window.py  # Example
```

- To run a specific test of a module:

```bash
pytest unit/core/test_window.py::test_window_fullscreen  # Example
```

> If you're in the root directory, make sure to add `tests/` to the path argument (e.g. `pytest tests/unit/core/test_window.py`).

## Information

Developed by [SammygoodTunes](https://github.com/SammygoodTunes)

Tested on Debian 12 and Windows 10

Libraries used: PyTest 8.3.3
