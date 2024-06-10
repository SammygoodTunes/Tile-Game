
from game.entity.player import Player
from game.utils.logger import logger


class PlayerHandler:
    """
    Class for creating the player handler.
    """

    def __init__(self) -> None:
        self._players: list[dict] = list()

    def track_player(self, player: dict) -> str:
        """
        Track the specified player by adding them to the players list.
        """
        self._players.append(player)
        logger.info(f'{player["name"]} joined the server.')
        print(f'Welcome, {player["name"]}!')
        return player['name']

    def update_player(self, player: dict) -> None:
        """
        Update the player attributes with the received player object, if possible.
        """
        if player is None:
            return
        logger.debug(f'Updating player \'{player["name"]}\'')
        index = next((i for i, p in enumerate(self._players) if p['name'] == player['name']), None)
        if index is None:
            self.track_player(player)
            return
        self._players[index]['previous_x'] = self._players[index]['x']
        self._players[index]['previous_y'] = self._players[index]['y']
        self._players[index]['x'] = player['x']
        self._players[index]['y'] = player['y']
        self._players[index]['pointing_at'] = player['pointing_at']
        self._players[index]['health'] = player['health']
        self._players[index]['holding_item'] = player['holding_item']

    def untrack_player(self, player_name: str) -> None:
        """
        Untrack the player by removing them from the players list, if possible.
        """
        logger.debug(f'Untracking player \'{player_name}\'')
        index = next((i for i, p in enumerate(self._players) if p['name'] == player_name), None)
        if index is None:
            logger.debug(f'Player \'{player_name}\' could not be untracked, as they were not found in the player list.')
            return
        self._players.pop(index)
        logger.info(f'{player_name} left the server.')

    def get_players(self) -> list[dict]:
        """
        Return the players list.
        """
        return self._players

    def get_player(self, player_name: str) -> dict | None:
        """
        Return player dict by player name if they exist, None otherwise.
        """
        index = next((i for i, p in enumerate(self._players) if p['name'] == player_name), None)
        if index is not None:
            return self._players[index]
        return None
