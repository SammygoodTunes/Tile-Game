"""
Integrated tests.
"""
from game.data.properties.world_properties import WorldProperties
from game.world.map_manager import Map


def test_map_get_tile():
    """
    Test: map_get_tile
    Desc: Tests if the map manager works as intended.
    Rqmt: Must return the correct tile based on the tile coordinates it is given.
    """
    dummy_map = Map(WorldProperties.MIN_MAP_WIDTH, WorldProperties.MIN_MAP_HEIGHT)
    dummy_map.generate()
