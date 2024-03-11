
from importlib import resources as impr

from game import data

# KEY=VALUE
GAME_PROPERTIES_FILE = impr.files(data) / "catchncage.properties"
GAME_PROPERTIES_SEPARATOR = '='

APP_NAME = "APP_NAME"
APP_VERSION = "APP_VER"


def get_game_properties():
    with open(GAME_PROPERTIES_FILE, 'r', encoding='utf-8') as prop_file:
        for line in prop_file.readlines():
            yield line


def get_game_property(game_property: str):
    get_game_properties_gen = get_game_properties()
    prop = next(get_game_properties_gen, None)
    while prop is not None:
        key, value = prop.split(GAME_PROPERTIES_SEPARATOR)
        if key == game_property:
            return value
        prop = next(get_game_properties_gen, None)
    return str()
