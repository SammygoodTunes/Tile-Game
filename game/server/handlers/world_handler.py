from typing import Self

from game.data.structures.player_structure import PlayerStructure
from game.data.tiles.tiles import Tiles
from game.network.builders.player_builder import PlayerBuilder
from game.utils.logger import logger
from game.world.world import World


class WorldHandler:
    """
    Class for a creating the world handler.
    """

    def __init__(self) -> None:
        self._world: World = World()
        self._queue: bytes = b''

    def create_world(self, seed: str) -> None:
        """
        Create a new server world.
        """
        self._world.create(seed)

    def update_broken_tile(self, player_dict: dict) -> None:
        """
        Update the map's tile data with the received player dict to take into account a broken tile.
        """
        _map = self._world.get_map()
        x, y = player_dict[PlayerBuilder.BROKEN_TILE_X], player_dict[PlayerBuilder.BROKEN_TILE_Y]
        logger.info(
            f'Player [{player_dict[PlayerBuilder.NAME_KEY]}] broke tile: '
            + f'{_map.get_tile(x, y)} '
            + f'at {x=} {y=}'
        )

        _map.set_tile(player_dict[PlayerBuilder.BROKEN_TILE_X], player_dict[PlayerBuilder.BROKEN_TILE_Y], Tiles.PLAINS)
        _map.set_dynatile(player_dict[PlayerBuilder.BROKEN_TILE_X], player_dict[PlayerBuilder.BROKEN_TILE_Y], True)
        self._queue += int.to_bytes(
                player_dict[PlayerBuilder.BROKEN_TILE_X],
                length=PlayerStructure.PLAYER_BROKEN_TILE_X_BYTE_SIZE
        ) + int.to_bytes(
                player_dict[PlayerBuilder.BROKEN_TILE_Y],
                length=PlayerStructure.PLAYER_BROKEN_TILE_Y_BYTE_SIZE
        )

    def is_queue_empty(self) -> bool:
        """
        Return True if queue is empty, otherwise False.
        """
        return not self._queue

    def clean_queue(self) -> Self:
        """
        Clears the queue.
        """
        self._queue = b''
        return self

    def get_queue(self) -> bytes:
        """
        Return the full queue in bytes.
        """
        return self._queue

    def get_world(self) -> World:
        """
        Return the world object.
        """
        return self._world