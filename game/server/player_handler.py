
from game.entity.player import Player


class PlayerHandler:
    """
    Class for creating the player handler.
    """

    def __init__(self):
        self._players: list[dict] = list()

    def track_player(self, player: dict) -> str:
        self._players.append(player)
        print(f'Welcome, {player["name"]}!')
        return player['name']

    def update_player(self, player: dict):
        index = next((i for i, p in enumerate(self._players) if p['name'] == player['name']), None)
        self._players[index] = player

    def untrack_player(self, player_name: str):
        index = next((i for i, p in enumerate(self._players) if p['name'] == player_name), None)
        self._players.pop(index)

    def get_players(self):
        return self._players
