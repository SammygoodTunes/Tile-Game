
import crayons


def error(message: str) -> None:
    """
    Print an error message in red.
    """
    print(crayons.red(message, bold=True))


def warning(message: str) -> None:
    """
    Print a warning message in yellow.
    """
    print(crayons.yellow(message, bold=True))


def success(message: str) -> None:
    """
    Print a success message in green.
    """
    print(crayons.green(message, bold=True))
