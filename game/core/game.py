"""
Module name: game

The game module is where all game-related tasks are run.
"""

import pygame

from game.client.client import Client
from game.core.window import Window
from game.gui.screen_manager import Screens
from game.server.server import Server


class Game(Window):
    """
    Class for managing a game instance.
    """

    def __init__(self, window_width: int, window_height: int) -> None:
        super().__init__(window_width, window_height)
        self._running: bool = True
        self.start_game: bool = False
        self.screens: Screens = Screens(self)
        self.client = Client()
        self.server = Server()
        self.client.initialise(self)
        self.update_all_uis()
        pygame.scrap.init()
        pygame.scrap.set_mode(pygame.SCRAP_CLIPBOARD)

    def update(self) -> None:
        """
        Update all child objects and core of the game.
        """
        self.window_updates()
        self.client.update(self)
        self.server.safe_closure()
        self.all_events()
        self.screens.update()
        self.draw_fps()
        self.tick()

    def window_updates(self) -> None:
        """
        Update window based on options' menu.
        """
        if self.vsync != self.screens.options_screen.vsync_box.is_checked():
            self.vsync = self.screens.options_screen.vsync_box.is_checked()
            self.screen = pygame.display.set_mode(
                (self.width, self.height),
                (pygame.HWACCEL | pygame.FULLSCREEN if self.fullscreen else pygame.RESIZABLE),
                depth=8,
                vsync=self.vsync
            )

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
                self.focused = True
                if e.key in [pygame.K_RETURN, pygame.K_KP_ENTER] and pygame.key.get_mods() & pygame.KMOD_ALT:
                    self.toggle_fullscreen()
                    self.update_all_uis()
                    continue
            elif e.type in [
                pygame.WINDOWRESIZED,
                pygame.WINDOWSIZECHANGED
            ]:
                if hasattr(e, 'x') and hasattr(e, 'y'):
                    self.resize(e)
                self.update_all_uis()
                self.focused = False
                pygame.event.clear(pygame.KEYDOWN)
                continue
            elif e.type == pygame.WINDOWMOVED:
                self.focused = False
                pygame.event.clear(pygame.KEYDOWN)
            self.client.events(self, e)
            self.screens.events(e)

    def update_all_uis(self) -> None:
        """
        Update all the GUI-related elements.
        """
        self.fps_label.update(self)
        self.screens.update_ui()
        self.client.update_ui()

    def draw_fps(self) -> None:
        """
        Update and draw the FPS on-screen.
        """
        if self.screens.options_screen.show_fps_box.is_checked():
            if self.timer != pygame.time.get_ticks() // 1000:
                self.fps_label.set_text(f"FPS: {self.clock.get_fps(): .0f}")
                self.timer = pygame.time.get_ticks() // 1000
            self.fps_label.set_x(self.width - self.fps_label.get_width() - 4)
            self.fps_label.set_y(-8)
            self.fps_label.draw(self.screen)

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
                if e.type in [
                    pygame.WINDOWRESIZED,
                    pygame.WINDOWSIZECHANGED
                ]:
                    self.resize(e)
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

