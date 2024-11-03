"""
Module name: player_manager

This module manages the local player and the local player list received from the server's global game state,
as well as rendering the other players to the screen.
"""

from __future__ import annotations
from pygame.draw import rect
from pygame.math import lerp
from typing import Self, TYPE_CHECKING

if TYPE_CHECKING: from game.core.game import Game
from game.entity.player import Player
from game.gui.nametag import NameTag
from game.network.builders.player_builder import PlayerBuilder


class PlayerManager:
    """
    Class for handling client player information.
    """

    def __init__(self, player) -> None:
        self.local_player: Player = player
        self.players: list = []

    def set_players(self, players: list | bytes | None) -> Self:
        """
        Set the players list and return the player manager itself.
        """
        if players is None:
            return self
        if isinstance(players, bytes):
            data_pos = players.index(b'\x00') + 1
            lengths = list(players[:data_pos - 1])
            decompressed_players = []
            for length in lengths:
                decompressed_players.append(PlayerBuilder.decompress_player(players[data_pos:data_pos + length]))
                data_pos += length
            self.players = decompressed_players
            return self
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

    def draw_players(self, player_name: str, delta: float, game: Game) -> None:
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
            nametag.resize(game)
            nametag.set_x(screen_x + 16 - nametag.get_width() // 2)
            nametag.update(game)
            nametag.set_state(True)
            nametag.draw(game.screen)
