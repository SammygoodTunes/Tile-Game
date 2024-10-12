from time import time

from game.data.structures.player_structure import (PlayerStructure)


class BaseBuilder:
    """
    Base class for packet building
    """
    COMMAND_ID_KEY = 'id'
    TIMESTAMP_KEY = 'timestamp'

    (
        PLAYER_POSITION_UPDATE_COMMAND
    ) = 0


class PlayerBuilder:
    """
    Class for the player packet builder.
    """
    NAME_KEY = 'name'
    X_POS_KEY = 'x'
    Y_POS_KEY = 'y'
    PREV_X_POS_KEY = 'previous_x'
    PREV_Y_POS_KEY = 'previous_y'
    LERP_KEY = 'lerp'
    HEALTH_KEY = 'health'

    @staticmethod
    def create_player() -> dict:
        """
        Create a player packet.
        """
        return {
            PlayerBuilder.NAME_KEY: '',
            PlayerBuilder.X_POS_KEY: 0,
            PlayerBuilder.Y_POS_KEY: 0,
            PlayerBuilder.PREV_X_POS_KEY: 0,
            PlayerBuilder.PREV_Y_POS_KEY: 0,
            PlayerBuilder.LERP_KEY: 0.0,
            PlayerBuilder.HEALTH_KEY: 100,
        }

    @staticmethod
    def build_player(player, player_dict: dict) -> None:
        """
        Build the player object from a player packet.
        """
        player.set_player_name(player_dict[PlayerBuilder.NAME_KEY])
        player.set_x(player_dict[PlayerBuilder.X_POS_KEY])
        player.set_y(player_dict[PlayerBuilder.Y_POS_KEY])
        player.set_health(player_dict[PlayerBuilder.HEALTH_KEY])

    @staticmethod
    def build_player_update_position_packet(player) -> dict:
        """
        Create an empty player position update packet.
        """
        return {
            BaseBuilder.COMMAND_ID_KEY: BaseBuilder.PLAYER_POSITION_UPDATE_COMMAND,
            BaseBuilder.TIMESTAMP_KEY: time(),
            PlayerBuilder.NAME_KEY: player.get_player_name(),
            PlayerBuilder.X_POS_KEY: player.get_x(),
            PlayerBuilder.Y_POS_KEY: player.get_y()
        }

    @staticmethod
    def compress_player(player: dict) -> bytes:
        """
        Compress a player dict into small, compact bytes object.
        TODO: Use UUIDs instead of names
        """
        name = b''.join(int.to_bytes(ord(c) - ord('-') + 2) for c in player[PlayerBuilder.NAME_KEY])
        x = int.to_bytes(round(player[PlayerBuilder.X_POS_KEY]), length=PlayerStructure.PLAYER_X_BYTE_SIZE, signed=True)
        y = int.to_bytes(round(player[PlayerBuilder.Y_POS_KEY]), length=PlayerStructure.PLAYER_Y_BYTE_SIZE, signed=True)
        prev_x = int.to_bytes(round(player[PlayerBuilder.PREV_X_POS_KEY]), length=PlayerStructure.PLAYER_X_BYTE_SIZE, signed=True)
        prev_y = int.to_bytes(round(player[PlayerBuilder.PREV_Y_POS_KEY]), length=PlayerStructure.PLAYER_Y_BYTE_SIZE, signed=True)
        lerp = int.to_bytes(int(player[PlayerBuilder.LERP_KEY] * 100))
        health = int.to_bytes(player[PlayerBuilder.HEALTH_KEY])

        return (
            name
            + b'\x01'
            + x
            + y
            + prev_x
            + prev_y
            + lerp
            + health
        )

    @staticmethod
    def decompress_player(bytes_obj: bytes) -> dict:
        """
        Decompress a player bytes object back to a player dict.
        """
        name_pos = bytes_obj.index(b'\x01')
        x_pos = name_pos + 1
        y_pos = x_pos + PlayerStructure.PLAYER_X_BYTE_SIZE
        prev_x_pos = y_pos + PlayerStructure.PLAYER_Y_BYTE_SIZE
        prev_y_pos = prev_x_pos + PlayerStructure.PLAYER_X_BYTE_SIZE
        lerp_pos = prev_y_pos + PlayerStructure.PLAYER_Y_BYTE_SIZE
        health_pos = lerp_pos + 1

        return {
            PlayerBuilder.NAME_KEY: ''.join(chr(c + ord('-') - 2) for c in bytes_obj[:name_pos]),
            PlayerBuilder.X_POS_KEY: int.from_bytes(bytes_obj[x_pos:x_pos + PlayerStructure.PLAYER_X_BYTE_SIZE], signed=True),
            PlayerBuilder.Y_POS_KEY: int.from_bytes(bytes_obj[y_pos:y_pos + PlayerStructure.PLAYER_Y_BYTE_SIZE], signed=True),
            PlayerBuilder.PREV_X_POS_KEY: int.from_bytes(bytes_obj[prev_x_pos:prev_x_pos + PlayerStructure.PLAYER_X_BYTE_SIZE], signed=True),
            PlayerBuilder.PREV_Y_POS_KEY: int.from_bytes(bytes_obj[prev_y_pos:prev_y_pos + PlayerStructure.PLAYER_Y_BYTE_SIZE], signed=True),
            PlayerBuilder.LERP_KEY: int.from_bytes(bytes_obj[lerp_pos:lerp_pos + 1]),
            PlayerBuilder.HEALTH_KEY: int.from_bytes(bytes_obj[health_pos:health_pos + 1])
        }
