
import crayons


def error(message: str):
    print(crayons.red(message, bold=True))


def warning(message: str):
    print(crayons.yellow(message, bold=True))


def success(message: str):
    print(crayons.green(message, bold=True))
