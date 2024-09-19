
from time import time


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
    POINTING_AT_POS_KEY = 'pointing_at'
    HEALTH_KEY = 'health'
    HOLDING_ITEM_KEY = 'holding_item'
    DIRECTION_KEY = 'direction'
    VELOCITY_KEY = 'velocity'
    DATA_KEY = 'data'

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
            PlayerBuilder.POINTING_AT_POS_KEY: (0, 0),
            PlayerBuilder.HEALTH_KEY: 100,
            PlayerBuilder.HOLDING_ITEM_KEY: None
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
