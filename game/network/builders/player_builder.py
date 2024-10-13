from game.data.structures.player_structure import PlayerStructure
from game.network.builders.base_builder import BaseBuilder


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
    BROKEN_TILE_X = 'broken_tile_x'
    BROKEN_TILE_Y = 'broken_tile_y'

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
    def get_compressed_player_packet(command_id: int, player) -> bytes:
        """
        Return a compressed update player packet from the attributes of the given player object.
        """
        assert 0 <= command_id <= BaseBuilder.COMMAND_ID_MAX, f'Invalid command ID: {command_id}'
        base = (
            int.to_bytes(command_id + BaseBuilder.COMMAND_ID_OFFSET)
            + b''.join(int.to_bytes(ord(c) - ord('-') + 2) for c in player.get_player_name())
        )
        if command_id == BaseBuilder.PLAYER_POSITION_UPDATE_COMMAND:
            x = int.to_bytes(round(player.get_x()), length=PlayerStructure.PLAYER_X_BYTE_SIZE, signed=True)
            y = int.to_bytes(round(player.get_y()), length=PlayerStructure.PLAYER_Y_BYTE_SIZE, signed=True)
            return base + b'\x01' + x + y
        if command_id == BaseBuilder.PLAYER_TILE_BREAK_COMMAND:
            broken_tile_x = int.to_bytes(
                player.prev_broken_tile[0],
                length=PlayerStructure.PLAYER_BROKEN_TILE_X_BYTE_SIZE
            )
            broken_tile_y = int.to_bytes(
                player.prev_broken_tile[1],
                length=PlayerStructure.PLAYER_BROKEN_TILE_Y_BYTE_SIZE
            )
            return base + b'\x01' + broken_tile_x + broken_tile_y

    @staticmethod
    def get_decompressed_player_packet(bytes_obj: bytes) -> dict:
        """
        Return a player dict from a player bytes object.
        """
        type_id = bytes_obj[0] - BaseBuilder.COMMAND_ID_OFFSET
        assert 0 <= type_id <= BaseBuilder.COMMAND_ID_MAX, f'Invalid command ID: {bytes_obj[0]}'
        name_pos = bytes_obj.index(b'\x01') + 1
        if type_id == BaseBuilder.PLAYER_POSITION_UPDATE_COMMAND:
            x_pos = name_pos
            y_pos = x_pos + PlayerStructure.PLAYER_X_BYTE_SIZE
            return {
                PlayerBuilder.NAME_KEY: ''.join(chr(c + ord('-') - 2) for c in bytes_obj[1:bytes_obj.index(b'\x01')]),
                PlayerBuilder.X_POS_KEY: int.from_bytes(bytes_obj[x_pos:x_pos + PlayerStructure.PLAYER_X_BYTE_SIZE], signed=True),
                PlayerBuilder.Y_POS_KEY: int.from_bytes(bytes_obj[y_pos:y_pos + PlayerStructure.PLAYER_Y_BYTE_SIZE], signed=True),
            }
        if type_id == BaseBuilder.PLAYER_TILE_BREAK_COMMAND:
            broken_tile_x_pos = name_pos
            broken_tile_y_pos = broken_tile_x_pos + PlayerStructure.PLAYER_BROKEN_TILE_X_BYTE_SIZE
            return {
                PlayerBuilder.NAME_KEY: ''.join(chr(c + ord('-') - 2) for c in bytes_obj[1:bytes_obj.index(b'\x01')]),
                PlayerBuilder.BROKEN_TILE_X: int.from_bytes(
                    bytes_obj[broken_tile_x_pos:broken_tile_x_pos + PlayerStructure.PLAYER_BROKEN_TILE_X_BYTE_SIZE]
                ),
                PlayerBuilder.BROKEN_TILE_Y: int.from_bytes(
                    bytes_obj[broken_tile_y_pos:]
                ),
            }

    @staticmethod
    def update_player_from_packet(bytes_obj: bytes, player) -> None:
        """
        Automatically update a player object from a player bytes object.
        """
        player_dict = PlayerBuilder.get_decompressed_player_packet(bytes_obj)
        if PlayerBuilder.NAME_KEY in player_dict:
            player.set_player_name(player_dict.get(PlayerBuilder.NAME_KEY))
        if PlayerBuilder.X_POS_KEY in player_dict:
            player.set_x(player_dict.get(PlayerBuilder.X_POS_KEY))
        if PlayerBuilder.Y_POS_KEY in player_dict:
            player.set_y(player_dict.get(PlayerBuilder.Y_POS_KEY))

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
