
from time import time


class BaseBuilder:
    """
    Base class for packet building
    """

    COMMAND_ID_KEY = 'id'
    TIMESTAMP_KEY = 'timestamp'

    (
        PLAYER_MOVE_COMMAND_ID
    ) = 1


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
    def build_player_move():
        """
        Build a player move packet.
        """
        return {
            BaseBuilder.COMMAND_ID_KEY: BaseBuilder.PLAYER_MOVE_COMMAND_ID,
            BaseBuilder.TIMESTAMP_KEY: time(),
            PlayerBuilder.NAME_KEY: '',
            PlayerBuilder.DIRECTION_KEY: 0
        }


