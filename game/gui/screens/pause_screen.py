
from pygame import Surface

from game.gui.screens.screen import Screen
from game.gui.label import Label
from game.gui.button import Button
from game.utils.logger import logger


class PauseScreen(Screen):
    """
    Class for creating the pause screen.
    """

    def __init__(self, window) -> None:
        super().__init__()
        self.window = window
        self.faded_surface = self.initialise_surface()
        self.pause_label = Label(text="Paused").center_horizontally(0, window.width)
        self.resume_button = Button(text="Resume").center_horizontally(0, window.width).center_vertically(0, window.height).offset_y(-75)
        self.options_button = Button(text="Options").center_horizontally(0, window.width).center_vertically(0, window.height)
        self.quit_button = Button(text="Quit").center_horizontally(0, window.width).center_vertically(0, window.height).offset_y(75)
        logger.debug(f'Created {__class__.__name__} with attributes {self.__dict__}')

    def initialise_surface(self) -> Surface:
        """
        Initialise the screen's surface.
        """
        surface = Surface((self.window.width, self.window.height))
        surface.fill((0, 0, 0))
        surface.set_alpha(96)
        return surface

    def draw(self) -> None:
        """
        Draw the screen and its components.
        """
        if self._enabled:
            self.window.screen.blit(self.faded_surface, (0, 0))
            self.pause_label.draw(self.window.screen)
            self.resume_button.draw(self.window.screen)
            self.options_button.draw(self.window.screen)
            self.quit_button.draw(self.window.screen)

    def update_ui(self) -> None:
        """
        Update the screen UI.
        """
        self.pause_label.update(self.window)
        self.pause_label.center_with_offset(0, 0, self.window.width, self.window.height, 0, -self.options_button.get_height() - 25 - self.pause_label.font.size(self.pause_label.get_text())[1])
        self.faded_surface = self.initialise_surface()
        self.resume_button.update(self.window)
        self.resume_button.center_with_offset(0, 0, self.window.width, self.window.height, 0, -self.quit_button.get_height() - 5)
        self.options_button.update(self.window)
        self.options_button.center(0, 0, self.window.width, self.window.height)
        self.quit_button.update(self.window)
        self.quit_button.center_with_offset(0, 0, self.window.width, self.window.height, 0, self.options_button.get_height() + 5)

    def set_state(self, state: bool) -> None:
        """
        Set the screen's visibility/interactivity.
        """
        super().set_state(state)
        self.pause_label.set_state(state)
        self.resume_button.set_state(state)
        self.options_button.set_state(state)
        self.quit_button.set_state(state)
