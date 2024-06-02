
from pygame.math import lerp, clamp
from pygame.draw import rect
from typing import Self

from game.data.properties import ServerProperties
from game.gui.label import Label
from game.gui.nametag import NameTag


class PlayerManager:
    """
    Class for handling server players.
    """

    def __init__(self) -> None:
        self.players = list()

    def set_players(self, players: list) -> Self:
        """
        Set the players list and return the player manager itself.
        """
        self.players = players
        return self

    def draw_players(self, player_name: str, delta: float, game) -> None:
        """
        Draw to the screen each player present in the players list.
        """
        for player in self.players:
            if player['name'] != player_name:
                player['lerp'] = round(clamp(player['lerp'] + delta / (1 / ServerProperties.TICKS_PER_SECOND), 0.0, 1.0), 3)
                screen_x = game.width / 2 - game.camera.x + lerp(player['previous_x'], player['x'], player['lerp'])
                screen_y = game.height / 2 - game.camera.y + lerp(player['previous_y'], player['y'], player['lerp'])
                rect(game.screen, (200, 200, 220), (screen_x, screen_y, 32, 32))
                nametag = NameTag(text=player['name'], x=screen_x - 10, y=screen_y - 16)
                nametag.set_state(True)
                nametag.update(game)
                nametag.draw(game.screen)
