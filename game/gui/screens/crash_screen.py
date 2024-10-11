
from pygame import Surface

from game.gui.screens.screen import Screen
from game.gui.label import Label
from game.utils.logger import logger


class CrashScreen(Screen):
    """
    Class for creating the crash screen.
    """

    def __init__(self, window) -> None:
        super().__init__()
        self.window = window
        self.surface = self.initialise_surface()
        self.crash_label = Label(text="The game crashed").center_horizontally(0, window.width)
        self.traceback_label = Label().set_colour((255, 50, 50)).set_shadow_colour((50, 0, 00))

    def initialise_surface(self) -> Surface:
        """
        Initialise the screen's surface.
        """
        surface = Surface((self.window.width, self.window.height))
        surface.fill((0, 0, 0))
        return surface

    def draw(self) -> None:
        """
        Draw the screen and its components.
        """
        if self._enabled:
            self.window.screen.blit(self.surface, (0, 0))
            self.traceback_label.draw(self.window.screen)
            self.crash_label.draw(self.window.screen)

    def update_ui(self) -> None:
        """
        Update the screen UI.
        """
        self.crash_label.update(self.window)
        self.crash_label.set_y(24).center_horizontally(0, self.window.width)
        self.traceback_label.update(self.window)
        self.traceback_label.set_x(24).set_y(48)
        self.surface = self.initialise_surface()

    def set_state(self, state: bool) -> None:
        """
        Set the screen's visibility/interactivity.
        """
        super().set_state(state)
        self.crash_label.set_state(state)
        self.traceback_label.set_state(state)
