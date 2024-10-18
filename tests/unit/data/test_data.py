"""
Tests dedicated to the data modules.
"""

from game.data.items.item import Item
from game.data.states.mouse_states import MouseStates
from game.data.tiles.tile import Tile


def test_item_creation():
    """
    Test: item_creation
    Desc: Tests if items are created correctly.
    Rqmt: All attributes must be equaled to the values they were given.
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
    Desc: Tests if the mouse properties possess the correct values.
    Rqmt: The mouse states must be equaled to their defined values.
    """
    assert (MouseStates.LMB, MouseStates.MMB, MouseStates.RMB, MouseStates.SCROLL_UP, MouseStates.SCROLL_DOWN) == tuple(range(1, 6))


def test_tile_creation():
    """
    Test: tile_creation
    Desc: Tests if tiles are created correctly.
    Rqmt: All attributes must be
    """
    dummy_tile = Tile(x=5, y=4).set_resistance(150).set_damage(25).set_damage_delay(0.5)
    assert isinstance(dummy_tile, Tile)
    assert dummy_tile.get_xy() == (5, 4)
    assert dummy_tile.get_resistance() == 150
    assert dummy_tile.get_damage() == 25
    assert dummy_tile.get_damage_delay() == 0.5

def test_tile_creation_failure():
    """

    """


def test_tile_compression():
    """
    Test: map_compression
    Desc: Tests if the map compression and decompression algorithms work as intended.
    """
    dummy_tile = Tile(x=5, y=7).set_resistance(50).set_damage(4).set_damage_delay(0.1)
    compressed_tile_value = dummy_tile.compress()
    decompressed_tile = Tile().decompress(compressed_tile_value)
    assert dummy_tile == decompressed_tile
