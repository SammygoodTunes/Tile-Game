
from pygame.math import lerp, clamp
from pygame.draw import rect
from typing import Self

from game.data.items.items import Items
from game.data.properties.server_properties import ServerProperties
from game.entity.player import Player
from game.gui.nametag import NameTag
from game.network.builders import PlayerBuilder


class PlayerManager:
    """
    Class for handling client player information.
    """

    def __init__(self, player) -> None:
        self.local_player: Player = player
        self.players = list()

    def build_local_player(self, player_dict: dict):
        """
        Build the local player from a player packet.
        """
        PlayerBuilder.build_player(self.local_player, player_dict)

    def packetise_player(self) -> dict:
        """
        Return a data-complete player packet.
        """
        return PlayerBuilder.build_player_update_position_packet(self.local_player)

    def set_players(self, players: list | None) -> Self:
        """
        Set the players list and return the player manager itself.
        """
        if players is not None:
            self.players = players
        return self

    def get_player(self, player_name: str) -> dict | None:
        """
        Return the player by player name if they exist, None otherwise.
        """
        index = next((i for i, p in enumerate(self.players) if p['name'] == player_name), None)
        if index is not None:
            return self.players[index]
        return None

    def hit_player(self, player_name: str) -> str:
        """
        Check and return the player that has been hit.
        """
        player = self.get_player(player_name)
        if player is None:
            return str()
        for p in self.players:
            if p['name'] == player['name']:
                continue
            if (p['x'] <= player['pointing_at'][0] <= p['x'] + 32
                    and p['y'] <= player['pointing_at'][1] <= p['y'] + 32
                    and player['holding_item'] == Items.GUN):
                return p['name']
        return str()

    def draw_players(self, player_name: str, delta: float, game) -> None:
        """
        Draw to the screen each player present in the players list.
        """
        for player in self.players:
            if player['name'] == player_name:
                continue
            #player['lerp'] = round(clamp(player['lerp'] + 0.1, 0.0, 1.0), 3)
            screen_x = round(game.width // 2 - int(game.client.camera.x) + round(lerp(player['previous_x'], player['x'], player['lerp']), 2))
            screen_y = round(game.height // 2 - int(game.client.camera.y) + round(lerp(player['previous_y'], player['y'], player['lerp']), 2))
            rect(game.screen, (200, 200, 220), (screen_x, screen_y, 32, 32))
            nametag = NameTag(text=player['name'], x=screen_x, y=screen_y - 20)
            nametag.set_x(screen_x + 16 - nametag.get_width() // 2)
            nametag.set_state(True)
            nametag.update(game)
            nametag.draw(game.screen)
