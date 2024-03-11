"""
Tests dedicated to the data modules.
"""

from importlib import resources as impr
from os.path import isfile

from game import data
from game.data.data_manager import (
    get_game_properties,
    get_game_property,
    GAME_PROPERTIES_FILE,
    GAME_PROPERTIES_SEPARATOR,
    APP_NAME,
    APP_VERSION)
from game.data.items import Item
from game.data.mouse_properties import Mouse
from game.data.tiles import Tile

DATA_DIR = impr.files(data)


def test_data_folder_exists():
    """
    Test: data_folder_exists
    Desc: Tests if the data folder exists.
    """
    assert DATA_DIR.is_dir()


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


def test_item_creation():
    """
    Test: item_creation
    Desc: Tests if items are created correctly.
    """
    dummy_item = (Item(x=2 ** 5, y=2 ** 7, tooltip_name='Dummy Item')
                  .set_strength(100).set_durability(50))
    assert isinstance(dummy_item, Item)
    assert dummy_item.get_xy() == (2 ** 5, 2 ** 7)
    assert dummy_item.get_tooltip_name() == 'Dummy Item'
    assert dummy_item.get_strength() == 100
    assert dummy_item.get_durability() == 50


def test_mouse_properties():
    """
    Test: mouse_properties
    Desc: Tests if the mouse properties possess the same values defined in Mouse.
    """
    assert (Mouse.LMB, Mouse.MMB, Mouse.RMB, Mouse.SCROLL_UP, Mouse.SCROLL_DOWN) == tuple(range(1, 6))


def test_tile_creation():
    """
    Test: tile_creation
    Desc: Tests if tiles are created correctly.
    """
    dummy_tile = Tile(x=2 ** 4, y=3 ** 5).set_resistance(150).set_damage(25).set_damage_delay(0.005)
    assert isinstance(dummy_tile, Tile)
    assert dummy_tile.get_xy() == (2 ** 4, 3 ** 5)
    assert dummy_tile.get_resistance() == 150
    assert dummy_tile.get_damage() == 25
    assert dummy_tile.get_damage_delay() == 0.005
