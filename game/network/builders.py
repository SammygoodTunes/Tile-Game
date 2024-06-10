
from game.entity.player import Player


class PlayerBuilder:
    """
    Class for building a player.
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

    @staticmethod
    def create_player() -> dict:
        """
        Build a server player.
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
    def build_player(player: Player, player_dict: dict) -> None:
        player.set_player_name(player_dict[PlayerBuilder.NAME_KEY])
        player.set_x(player_dict[PlayerBuilder.X_POS_KEY])
        player.set_y(player_dict[PlayerBuilder.Y_POS_KEY])
        player.set_health(player_dict[PlayerBuilder.HEALTH_KEY])
