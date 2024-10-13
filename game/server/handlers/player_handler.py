from game.network.builders.player_builder import PlayerBuilder
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
        if not player:
            return
        logger.debug(f'Updating player \'{player["name"]}\'')
        index = self.get_player(player['name'])['index']
        if index is None:
            return
        self._players[index]['previous_x'] = self._players[index]['x']
        self._players[index]['previous_y'] = self._players[index]['y']
        self._players[index]['x'] = player['x']
        self._players[index]['y'] = player['y']
        self._players[index]['health'] = player['health']

    def update_player_position(self, player_packet: dict) -> None:
        """
        Update the player position attribute with the received player packet, if possible.
        """
        if not player_packet:
            return
        index = self.get_player(player_packet['name'])['index']
        if index is None:
            self.track_player(player_packet)
            return
        self._players[index]['previous_x'] = self._players[index]['x']
        self._players[index]['previous_y'] = self._players[index]['y']
        self._players[index]['x'] = player_packet['x']
        self._players[index]['y'] = player_packet['y']

    def untrack_player(self, player_name: str) -> None:
        """
        Untrack the player by removing them from the players list, if possible.
        """
        logger.debug(f'Untracking player \'{player_name}\'')
        index = self.get_player(player_name)['index']
        if index is None:
            return
        self._players.pop(index)
        logger.info(f'{player_name} left the server.')

    def get_players(self, compressed=False) -> list[dict] | bytes:
        """
        Return the players list.
        """
        if compressed:
            return b''.join(
                int.to_bytes(len(PlayerBuilder.compress_player(player)))
                for player in self._players
            ) + b'\x00' + b''.join(
                PlayerBuilder.compress_player(player)
                for player in self._players
            )
        return self._players

    def get_player(self, player_name: str) -> dict[str, int | dict | None]:
        """
        Return player dict by player name if they exist, None otherwise.
        """
        index = next((i for i, p in enumerate(self._players) if p['name'] == player_name), None)
        if index is not None:
            return {'index': index, 'player': self._players[index]}
        logger.debug(f'Player \'{player_name}\' were not found in the player list.')
        return {'index': None, 'player': None}
