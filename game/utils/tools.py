
import crayons


def error(message: str):
    """
    Print an error message in red.
    """
    print(crayons.red(message, bold=True))


def warning(message: str):
    """
    Print a warning message in yellow.
    """
    print(crayons.yellow(message, bold=True))


def success(message: str):
    """
    Print a success message in green.
    """
    print(crayons.green(message, bold=True))
