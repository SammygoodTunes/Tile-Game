
from math import sin
import pygame

from game.client.client import Client
from game.core.window import Window
from game.data.data_manager import verify_game_property_values
from game.server.server import Server
from game.utils.logger import logger


class Game(Window):
    """
    Class for managing a game instance.
    """

    def __init__(self, window_width: int, window_height: int) -> None:
        super().__init__(window_width, window_height)
        self._running: bool = True
        self.start_game: bool = False
        self.screens.link_game(self)
        self.client = Client()
        self.server = Server()
        verify_game_property_values()
        self.client.initialise(self)
        self.update_all_uis()
        logger.debug(f'Created {__class__.__name__} with attributes {self.__dict__}')

    def update(self) -> None:
        """
        Update all child objects and core of the game.
        """
        self.client.update(self)
        self.all_events()
        self.screens.update()
        self.draw_fps() 
        self.tick()

    # Used for when game needs to be updated during threaded process
    # This should be used in a while loop controlled by an Event()
    def update_loop(self) -> None:
        """
        Like the standard update loop, but only used for threaded tasks.
        """
        self.all_events()
        self.screens.update()
        self.draw_fps()
        self.tick()

    def all_events(self) -> None:
        """
        Verify for any potential pygame events and update the targeted elements accordingly.
        """
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.stop()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN and pygame.key.get_mods() & pygame.KMOD_ALT:
                    self.toggle_fullscreen()
                    self.update_all_uis()
                    continue
            elif e.type == pygame.VIDEORESIZE:
                self.resize(e)
                self.update_all_uis()
                continue
            elif e.type == pygame.VIDEOEXPOSE:
                self.update_all_uis()
                continue
            self.client.events(self, e)
            self.screens.events(e)

    def update_all_uis(self) -> None:
        """
        Update all the GUI-related elements.
        """
        self.update_ui()
        self.client.update_ui()

    def is_running(self) -> bool:
        """
        Return the running state of the game.
        """
        return self._running

    def crash(self, traceback: str) -> None:
        """
        Initiate crash screen and stop any running process.
        Loop until user decides to quit the application.
        """
        self.stop()
        self.screens.crash_screen.set_state(True)
        self.screens.crash_screen.traceback_label.set_text(traceback)
        self.screens.crash_screen.update_ui()
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                if e.type == pygame.VIDEORESIZE:
                    self.resize(e)
                    self.screens.crash_screen.update_ui()
                    continue
                if e.type == pygame.VIDEOEXPOSE:
                    self.screens.crash_screen.update_ui()
            self.screens.crash_screen.draw()
            self.tick()
    
    def stop(self) -> None:
        """
        Terminate the game.
        """
        self._running = False
        self.client.stop()
        if self.server.sock:
            self.server.stop()

