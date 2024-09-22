
from math import sin
from pygame.event import Event
from pygame.time import get_ticks

from game.client.connection_handler import ConnectionHandler
from game.data.properties import CameraProperties, PlayerProperties, WorldProperties
from game.entity.player import Player
from game.world.camera import Camera
from game.world.world import World


class Client:
    """
    Class for all client-related tasks like client-side rendering and handling the connection.
    """

    def __init__(self):
        self.connection_handler = ConnectionHandler()
        self.camera: Camera = Camera(speed=CameraProperties.SPEED)
        self.player: Player = Player(speed=PlayerProperties.SPEED)
        self.world: World = World()

    def initialise(self, game) -> None:
        """
        Initialise the client.
        """
        self.player.init(game)

    def update(self, game) -> None:
        """
        Update the client.
        """
        ticks = get_ticks()
        self.connection_handler.update(game)
        if game.start_game:
            game.clear(WorldProperties.SKY_COLOUR)
            self.world.draw(game)
            # self.world.draw_wireframe(self.screen)
            self.connection_handler.draw_other_players(game, game.clock.get_time() / 1000.0)
            self.player.draw(game)
            self.player.draw_selection_grid(game)
            self.player.draw_gun_pointer(game)
            self.player.main_hud.draw()
            self.player.update(game, self.world.get_map())
            self.world.update(game, self.player)
            if not self.player.is_dead():
                self.camera.update(game)
            return
        game.clear((round(20 * sin(ticks / 5000) + 100), round(10 * sin(ticks / 2500) + 80), 150))

    def update_ui(self):
        """
        Update the client UI.
        """
        self.player.update_ui()
        self.world.update_ui()

    def events(self, game, e: Event):
        """
        Handle the client events.
        """
        if not game.paused and game.start_game:
            self.player.events(game, self.world.get_map(), e)

    def stop(self):
        """
        Stop the client connection.
        """
        if self.connection_handler.connection:
            self.connection_handler.connection.disconnect()
