
from pygame import Surface
from pygame.event import Event

from game.gui.screens.screen import Screen
from game.gui.progress_bar import ProgressBar
from game.utils.logger import logger


class LoadingScreen(Screen):
    """
    Class for creating the loading screen.
    """

    def __init__(self, window) -> None:
        super().__init__()
        self.window = window
        self.surface = self.initialise_surface()
        self.progress_bar = ProgressBar()

    def initialise_surface(self) -> Surface:
        """
        Initialise the screen's surface.
        """
        surface = Surface((self.window.width, self.window.height))
        surface.fill((0, 0, 0))
        return surface

    def events(self, e: Event) -> None:
        """
        Track the screen events (unused).
        """
        pass

    def draw(self) -> None:
        """
        Draw the screen and its components
        """
        if not self._enabled:
            return
        self.window.screen.blit(self.surface, (0, 0))
        self.progress_bar.draw(self.window.screen)

    def update_ui(self) -> None:
        """
        Update the screen UI.
        """
        if not self._enabled:
            return
        self.surface = self.initialise_surface()
        self.progress_bar.update(self.window)
        self.progress_bar.center(0, 0, self.window.width, self.window.height)

    def set_state(self, state: bool) -> None:
        """
        Set the screen's visibility/interactivity.
        """
        super().set_state(state)
        self.progress_bar.set_state(state)
        if state: self.update_ui()
