"""
Tests dedicated to the data modules.
"""

from importlib import resources as impr
from os.path import isfile

from game import assets
from game.data.data_manager import (
    get_game_properties,
    get_game_property,
    GAME_PROPERTIES_FILE,
    GAME_PROPERTIES_SEPARATOR,
    APP_NAME,
    APP_VERSION)

ASSETS_DIR = impr.files(assets)


def test_data_folder_exists():
    """
    Test: data_folder_exists
    Desc: Tests if the data folder exists.
    """
    assert ASSETS_DIR.is_dir()


def test_game_properties_file_exists():
    """
    Test: game_properties_file_exists
    Desc: Tests if the game properties file exists.
    """
    assert isfile(GAME_PROPERTIES_FILE)


def test_get_game_properties_exists():
    """
    Test: get_game_properties_exists
    Desc: Tests if all game property keys exist in the game properties file.
    """
    with open(GAME_PROPERTIES_FILE, 'r', encoding='utf-8') as prop_file:
        properties = [line.split(GAME_PROPERTIES_SEPARATOR)[0] for line in prop_file.readlines()]
        assert APP_NAME in properties
        assert APP_VERSION in properties


def test_get_game_properties():
    """
    Test: get_game_properties
    Desc: Tests if the get_game_properties function returns the correct keys and values.
    """
    get_game_properties_gen = get_game_properties()
    with open(GAME_PROPERTIES_FILE, 'r', encoding='utf-8') as prop_file:
        for line in prop_file.readlines():
            prop = next(get_game_properties_gen, None)
            key1, value1 = prop.split(GAME_PROPERTIES_SEPARATOR)
            key2, value2 = line.split(GAME_PROPERTIES_SEPARATOR)
            assert key1 == key2 and value1 == value2


def test_get_game_property():
    """
    Test: get_game_property
    Desc: Tests if the get_game_property function returns the correct value from the key it was given.
    """
    with open(GAME_PROPERTIES_FILE, 'r', encoding='utf-8') as prop_file:
        for line in prop_file.readlines():
            key, value = line.split(GAME_PROPERTIES_SEPARATOR)
            result = get_game_property(key)
            assert result == value
    assert not get_game_property("NONEXISTENT_PROPERTY")
