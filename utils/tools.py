
import crayons


def error(message: str):
    print(crayons.red(message, bold=True))


def warning(message: str):
    print(crayons.yellow(message, bold=True))


def success(message: str):
    print(crayons.green(message, bold=True))


def clamp(value: int, min_value: int, max_value: int):
    return max(min(value, max_value), min_value)


def world_to_screen(world_x: float, world_y: float, offset_x: float, offset_y: float):
    screen_x: int = int(world_x - offset_x)
    screen_y: int = int(world_y - offset_y)
    return screen_x, screen_y


def screen_to_world(screen_x: float, screen_y: float, offset_x: float, offset_y: float):
    world_x: float = float(screen_x + offset_x)
    world_y: float = float(screen_y + offset_y)
    return world_x, world_y
