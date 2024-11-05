"""
Module name: world_manager

This module manages the local world received from the server's global game state.
"""

from game.data.structures.map_structure import MapStructure
from game.network.packet import Compressor
from game.world.world import World


class WorldManager:
    """
    Class for handling client world information.
    """

    def __init__(self, world) -> None:
        self.local_world: World = world
        self.temp_data = b''

    def build_world_from_bytes(self, bytes_obj: bytes, update_map_size=False) -> None:
        """
        Build the local world from a world bytes object.
        """
        if not bytes_obj.strip():
            return
        bytes_obj = Compressor.decompress(bytes_obj)
        height_pos = MapStructure.MAP_WIDTH_BYTE_SIZE + MapStructure.MAP_HEIGHT_BYTE_SIZE
        width, height = (
            int.from_bytes(bytes_obj[:MapStructure.MAP_WIDTH_BYTE_SIZE]) + 1,
            int.from_bytes(bytes_obj[MapStructure.MAP_WIDTH_BYTE_SIZE:height_pos]) + 1
        )
        tile_data_pos_start = height_pos + MapStructure.MAP_TD_LEN_BYTE_SIZE
        length = int.from_bytes(bytes_obj[height_pos:tile_data_pos_start])

        if update_map_size:
            self.local_world.get_map().set_size_in_tiles(width, height)
            self.local_world.initialise()

        tile_data_pos_end = tile_data_pos_start + length
        compressed_tile_data = bytes_obj[tile_data_pos_start:tile_data_pos_end]
        if self.local_world.get_map().get_compressed_tile_data() != compressed_tile_data:
            self.local_world.get_map().set_compressed_tile_data(compressed_tile_data)
            self.local_world.get_map().decompress_tile_data()
        compressed_dynatile_data = bytes_obj[tile_data_pos_end:]
        self.temp_data = compressed_dynatile_data
