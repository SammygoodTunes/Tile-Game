from game.data.properties.tile_properties import TileProperties
from game.data.structures.map_structure import MapStructure
from game.data.structures.tile_structure import TileStructure
from game.data.tiles.tiles import Tiles
from game.network.builders.player_builder import PlayerBuilder
from game.world.map_manager import Map


class WorldManager:
    """
    Class for handling client world information.
    """

    def __init__(self, world) -> None:
        self.local_world = world
        self.queue_offset = 0

    def build_world_from_bytes(self, bytes_obj: bytes) -> None:
        """
        Build the local world from a world bytes object.
        """
        height_pos = MapStructure.MAP_WIDTH_BYTE_SIZE + MapStructure.MAP_HEIGHT_BYTE_SIZE
        width, height = (
            int.from_bytes(bytes_obj[:MapStructure.MAP_WIDTH_BYTE_SIZE]) + 1,
            int.from_bytes(bytes_obj[MapStructure.MAP_WIDTH_BYTE_SIZE:height_pos]) + 1
        )
        tile_data_pos = width * height * TileStructure.TILE_BYTE_SIZE + 2
        self.local_world.set_map(Map(width, height))
        self.local_world.get_map().set_tile_data(bytes_obj[height_pos:tile_data_pos])
        self.local_world.get_map().set_dynatile_data(bytes_obj[tile_data_pos:])

    def update_broken_tiles(self, bytes_obj: bytes) -> None:
        """
        Update the local map's tile data with the received player dict to take into account a broken tile.
        """
        if not bytes_obj:
            return
        for tile in range(0, len(bytes_obj), 2):
            # print(f"Set client side tile at: {bytes_obj[tile]} {bytes_obj[tile + 1]}")
            self.local_world.get_map().set_tile(bytes_obj[tile], bytes_obj[tile + 1], Tiles.PLAINS)
            self.local_world.get_map().set_dynatile(bytes_obj[tile], bytes_obj[tile + 1], True)
            self.local_world.get_map().tile_manager.draw(
                bytes_obj[tile] * TileProperties.TILE_SIZE,
                bytes_obj[tile + 1] * TileProperties.TILE_SIZE,
                Tiles.PLAINS,
                self.local_world.get_map().get_dynatile_surface()
            )
        self.queue_offset += len(bytes_obj)