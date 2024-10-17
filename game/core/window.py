"""
Module name: window

Here is where the game window is created and managed.
It handles game refreshes, updates from screen events (like resizing or fullscreen) and the GUI updates.
"""

import pygame

from game.client.managers.screen_manager import Screens
from game.data.properties.game_properties import GameProperties
from game.gui.label import Label
from game.utils.logger import logger
from game.utils.tools import resource_dir


class Window:
    """
    Class for creating the window frame in which the game will be contained.
    """

    FONT_PATH: str = resource_dir('game/assets/font.ttf')

    def __init__(self, width: int, height: int) -> None:
        self.width: int = width
        self.height: int = height
        self.old_width: int = width
        self.old_height: int = height
        self.max_width: int = pygame.display.Info().current_w
        self.max_height: int = pygame.display.Info().current_h
        self.screen: pygame.Surface | pygame.SurfaceType = pygame.display.set_mode(
            (self.width, self.height),
            pygame.RESIZABLE,
            depth=8,
            vsync=1)
        self.fps_cap: int = 200
        self.clock: pygame.time.Clock() = pygame.time.Clock()
        self.timer: int = 0
        self.font: pygame.font.Font = pygame.font.Font(Window.FONT_PATH, 11)
        self.screens: Screens = Screens(self)
        self.fps_label: Label = (Label(f"FPS: {str(round(self.clock.get_fps()))}", self.width - 75, -8))
        self.vsync: bool = True
        self.focused: bool = True
        self.paused: bool = False
        self.fullscreen: bool = False
        self.halt_refresh: bool = False  # used to prevent graphical distortion when resizing window
        pygame.display.set_caption(f'{GameProperties.APP_NAME} v{GameProperties.APP_VER}')

    def clear(self, colour: tuple[int, int, int]) -> None:
        """
        Clear the screen with the specified colour.
        """
        self.screen.fill(colour, (0, 0, self.width, self.height))

    def tick(self) -> None:
        """
        Refresh the screen and keep the in-game clock running.
        """
        if self.halt_refresh:
            self.halt_refresh = False
            return
        pygame.display.flip()
        self.clock.tick(self.fps_cap)

    def resize(self, e: pygame.event.Event) -> None:
        """
        Update window dimensions on resize.
        """
        self.halt_refresh = True
        logger.debug(f'Resizing screen to (W={e.x}, H={e.y}) from (W={self.width}, H={self.height})')
        if pygame.version.vernum >= (2, 0):
            self.screen = pygame.display.get_surface()
            self.width, self.height = self.screen.get_size()
        else:
            self.width, self.height = e.x, e.y
            self.screen = pygame.display.set_mode(
                (self.width, self.height),
                pygame.RESIZABLE,
                depth=8,
                vsync=self.vsync
            )

    def draw_fps(self) -> None:
        """
        Update and draw the FPS on-screen.
        """
        if self.screens.options_screen.show_fps_box.is_checked():
            if self.timer != pygame.time.get_ticks() // 1000:
                self.fps_label.set_text(f"FPS: {self.clock.get_fps(): .0f}")
                self.timer = pygame.time.get_ticks() // 1000
            self.fps_label.set_x(self.width - self.fps_label.get_total_width() - 4)
            self.fps_label.set_y(-8)
            self.fps_label.draw(self.screen)

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

    def update_ui(self) -> None:
        """
        Update all window GUI widgets.
        """
        self.fps_label.update(self)
        self.fps_label.refresh()
        self.screens.update_ui()

    def toggle_fullscreen(self) -> None:
        """
        Toggle between windowed mode and full-screen mode, and update the window accordingly.
        """
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.old_width = self.width
            self.old_height = self.height
            self.width, self.height = self.max_width, self.max_height
        else:
            self.width = self.old_width
            self.height = self.old_height
        self.screen = pygame.display.set_mode(
            (self.width, self.height),
            (pygame.HWACCEL | pygame.FULLSCREEN if self.fullscreen else pygame.RESIZABLE),
            depth=8,
            vsync=self.vsync
        )
