
from game.entity.player import Player


class PlayerHandler:
    """
    Class for creating the player handler.
    """

    def __init__(self):
        self._players: list[dict] = list()

    def track_player(self, player: dict):
        self._players.append(player)
        print(f'Welcome, {player["name"]}!')

    def update_player(self, player: dict):
        index = next((i for i, p in enumerate(self._players) if p['name'] == player['name']), None)
        self._players[index] = player

    def untrack_player(self, player_name: str):
        [self._players.remove(player) if player['name'] == player_name else None for player in self._players]

    def get_players(self):
        return self._players
