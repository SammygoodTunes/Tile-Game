"""
Integrated tests.
"""

from game.data.properties.world_properties import WorldProperties
from game.data.structures.tile_structure import TileStructure
from game.data.tiles.tiles import Tiles
from game.world.map_manager import Map

TEST_TILE = Tiles.LAVA


def test_map_get_tile():
    """
    Test: map_get_tile
    Desc: Tests if the map manager works as intended.
    Rqmt: Must return the correct tile based on the tile coordinates it is given.
    """
    dummy_map = Map(WorldProperties.MIN_MAP_WIDTH, WorldProperties.MIN_MAP_HEIGHT)
    dummy_map.set_tile_data(int.to_bytes(TEST_TILE.compress(), length=TileStructure.TILE_BYTE_SIZE))
    tile = dummy_map.get_tile(0, 0)
    assert tile == TEST_TILE
