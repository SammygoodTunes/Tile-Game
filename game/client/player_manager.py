
from pygame.draw import rect


class PlayerManager:
    """
    Class for handling server players.
    """

    def __init__(self):
        self.players = list()

    def set_players(self, players: list):
        self.players = players
        return self

    def draw_players(self, player_name: str, game):
        for player in self.players:
            if player["name"] != player_name:
                screen_x = game.width / 2 - game.camera.x + player['x']
                screen_y = game.height / 2 - game.camera.y + player['y']
                rect(game.screen, (200, 200, 220), (screen_x, screen_y, 32, 32))
