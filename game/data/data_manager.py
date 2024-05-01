
from importlib import resources as impr
from typing import Iterator

from game import data
from game.utils.exceptions import InvalidGamePropertyValue
from game.utils.logger import logger

# KEY=VALUE
GAME_PROPERTIES_FILE: str = str(impr.files(data) / "catchncage.properties")
GAME_PROPERTIES_SEPARATOR: str = '='

APP_NAME: str = "APP_NAME"
APP_VERSION: str = "APP_VER"
KEY_DELAY: str = "KEY_DELAY"
KEY_INTERVAL: str = "KEY_INTERVAL"


def get_game_properties() -> Iterator[str]:
    """
    Yield one game properties at a time from the game properties file.
    """
    with open(GAME_PROPERTIES_FILE, 'r', encoding='utf-8') as prop_file:
        for line in prop_file.readlines():
            yield line


def get_game_property(game_property: str) -> str:
    """
    Get the value of a specified game_property key.
    """
    key: str
    value: str
    get_game_properties_gen = get_game_properties()
    prop = next(get_game_properties_gen, None)
    logger.debug(f'Getting game property {game_property}.')
    while prop is not None:
        key, value = prop.split(GAME_PROPERTIES_SEPARATOR)
        if key == game_property:
            logger.debug(f'Value of property {game_property} found: {value}')
            return value.strip()
        prop = next(get_game_properties_gen, None)
    logger.warning(f'No value for property {game_property} found.')
    return str()


def verify_game_property_values():
    """
    Check that the game property values entered in the file follow the requirements.
    An exception is raised if one isn't followed.
    """
    if not get_game_property(KEY_DELAY).isnumeric():
        raise InvalidGamePropertyValue('KEY_DELAY must be an integer')
    if not get_game_property(KEY_INTERVAL).isnumeric():
        raise InvalidGamePropertyValue('KEY_INTERVAL must be an integer')
