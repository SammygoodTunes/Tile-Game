"""
Integrated tests.
"""

from game.client.managers.player_manager import PlayerManager
from game.client.managers.world_manager import WorldManager
from game.data.properties.world_properties import WorldProperties
from game.data.structures.tile_structure import TileStructure
from game.data.tiles.tiles import Tiles
from game.entity.player import Player
from game.network.builders.player_builder import PlayerBuilder
from game.network.packet import hex_len, Packet
from game.server.handlers.player_handler import PlayerHandler
from game.server.handlers.world_handler import WorldHandler
from game.world.map_manager import Map
from game.world.world import World

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

def test_tile_data_compression_equality():
    """
    Test: test_tile_data_compression_equality
    Desc: Tests if the decompressed map tile data is valid.
    Rqmt: The decompressed tile data must be equaled to the original tile data.
    """
    w, h = WorldProperties.MIN_MAP_WIDTH, WorldProperties.MIN_MAP_HEIGHT
    data = int.to_bytes(Tiles.DIRT.compress(), length=TileStructure.TILE_BYTE_SIZE)
    data += int.to_bytes(Tiles.DIRT.compress(), length=TileStructure.TILE_BYTE_SIZE)
    data += int.to_bytes(Tiles.LAVA.compress(), length=TileStructure.TILE_BYTE_SIZE)
    data += int.to_bytes(Tiles.WATER.compress(), length=TileStructure.TILE_BYTE_SIZE)
    data += int.to_bytes(Tiles.DIRT.compress(), length=TileStructure.TILE_BYTE_SIZE)
    data += int.to_bytes(Tiles.DIRT.compress(), length=TileStructure.TILE_BYTE_SIZE)
    data += int.to_bytes(Tiles.WATER.compress(), length=TileStructure.TILE_BYTE_SIZE)
    data += int.to_bytes(Tiles.DIRT.compress(), length=TileStructure.TILE_BYTE_SIZE)
    data += int.to_bytes(Tiles.LAVA.compress(), length=TileStructure.TILE_BYTE_SIZE)
    dummy_map = Map(w, h)
    dummy_map.set_tile_data(data)
    dummy_map.compress_tile_data()
    dummy_map.decompress_tile_data()
    assert dummy_map.get_tile_data() == data
