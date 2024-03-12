
from importlib import resources as impr
from importlib.abc import Traversable
import pygame

from game import assets
import game.data.data_manager as data_mng
from game.gui.label import Label
from game.gui.screen_manager import Screens


class Window:
    """
    Class for creating the window frame in which the game will be contained.
    """

    FONT_PATH: str = impr.files("assets") / "font.ttf"

    def __init__(self, width: int, height: int, title: str = data_mng.get_game_property(data_mng.APP_NAME)) -> None:
        self.width: int = width
        self.height: int = height
        self.old_width: int = width
        self.old_height: int = height
        self.max_width: int = pygame.display.Info().current_w
        self.max_height: int = pygame.display.Info().current_h
        self.screen: pygame.Surface | pygame.SurfaceType = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        self.fps_cap: int = 200
        self.clock: pygame.time.Clock() = pygame.time.Clock()
        self.timer: int = 0
        self.font: pygame.font.Font = pygame.font.Font(Window.FONT_PATH, 11)
        self.screens: Screens = Screens(self)
        self.fps_label: Label = (Label(f"FPS: {str(round(self.clock.get_fps()))}", self.width - 75, -8)
                                 .set_shadow_x(self.width - 73).set_shadow_y(-6)
                                 .set_colour((240, 240, 240)).set_shadow_colour((25, 25, 25)))
        self.paused: bool = False
        self.start_game: bool = False
        self.fullscreen: bool = False
        self.halt_refresh: bool = False  # used to prevent graphical distortion when resizing window
        pygame.display.set_caption(title)

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
        self.clock.tick_busy_loop(self.fps_cap)

    def resize(self, e: pygame.event.Event | pygame.event.EventType) -> None:
        """
        Update window dimensions on resize.
        """
        self.halt_refresh = True
        if pygame.version.vernum >= (2, 0):
            self.screen = pygame.display.get_surface()
            self.width, self.height = self.screen.get_size()
        else:
            self.width, self.height = e.w, e.h
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE | pygame.DOUBLEBUF)

    def draw_fps(self) -> None:
        """
        Update and draw the FPS on-screen.
        """
        if self.screens.options_screen.show_fps_box.is_checked():
            if self.timer != pygame.time.get_ticks() // 1000:
                self.fps_label.set_text(f"FPS: {self.clock.get_fps(): .0f}")
                self.timer = pygame.time.get_ticks() // 1000
            self.fps_label.draw(self.screen)

    def update_ui(self) -> None:
        """
        Update all window GUI widgets.
        """
        self.fps_label.set_auto_font_size(self.width, self.height, self.max_width, self.max_height)
        self.fps_label.set_x(self.width - (self.fps_label.get_font_size() * 7) - 4).set_shadow_x(self.width - (self.fps_label.get_font_size() * 7) - 4 - 2)
        self.fps_label.set_y(-self.fps_label.get_font_size() + 4).set_shadow_y(-self.fps_label.get_font_size() + 6)
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
            (self.width, self.height), pygame.FULLSCREEN if self.fullscreen else pygame.RESIZABLE
        )
