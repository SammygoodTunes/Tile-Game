
from game.entity.player import Player


def build_player(player: Player) -> dict:
    """
    Build a server player from a client player.
    """
    return {
        'name': player.get_player_name(),
        'x': player.get_x(),
        'y': player.get_y(),
        'previous_x': 0,
        'previous_y': 0,
        'lerp': 0.0
    }


def unbuild_player(player: Player, player_dict: dict) -> Player:
    """
    Un-build a server player to a client player.
    """
    return (player
            .set_player_name(player_dict['name'])
            .set_x(player_dict['x'])
            .set_y(player_dict['y'])
            )
