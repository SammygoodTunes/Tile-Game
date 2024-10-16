from numpy.distutils.misc_util import colour_text
from pygame import Surface

from game.data.properties.screen_properties import ScreenProperties
from game.gui.screens.screen import Screen
from game.gui.label import Label
from game.gui.button import Button


class PauseScreen(Screen):
    """
    Class for creating the pause screen.
    """

    def __init__(self, window) -> None:
        super().__init__()
        self.window = window
        self.faded_surface = self.initialise_surface()
        self.pause_label = Label(text="PAUSE MENU").set_colour((240, 240, 255)).center_horizontally(0, window.width).set_font_sizes((14, 15, 16))
        self.resume_button = Button(text="Resume").center_horizontally(0, window.width).center_vertically(0, window.height).offset_y(-75)
        self.options_button = Button(text="Options").center_horizontally(0, window.width).center_vertically(0, window.height)
        self.disconnect_button = Button(text="Disconnect").center_horizontally(0, window.width).center_vertically(0, window.height).offset_y(75)

    def initialise_surface(self) -> Surface:
        """
        Initialise the screen's surface.
        """
        surface = Surface((self.window.width, self.window.height))
        surface.fill((0, 0, 0))
        surface.set_alpha(ScreenProperties.ALPHA)
        return surface

    def draw(self) -> None:
        """
        Draw the screen and its components.
        """
        if not self._enabled:
            return
        self.window.screen.blit(self.faded_surface, (0, 0))
        self.pause_label.draw(self.window.screen)
        self.resume_button.draw(self.window.screen)
        self.options_button.draw(self.window.screen)
        self.disconnect_button.draw(self.window.screen)

    def update_ui(self) -> None:
        """
        Update the screen UI.
        """
        if not self._enabled:
            return
        self.pause_label.update(self.window)
        self.pause_label.center_with_offset(0, 0, self.window.width, self.window.height, 0, -self.options_button.get_height() - 25 - self.pause_label.font.size(self.pause_label.get_text())[1])
        self.faded_surface = self.initialise_surface()
        self.options_button.update(self.window)
        self.options_button.center(0, 0, self.window.width, self.window.height)
        self.disconnect_button.update(self.window)
        self.disconnect_button.center_with_offset(0, 0, self.window.width, self.window.height, 0, self.options_button.get_height() + 5)
        self.resume_button.update(self.window)
        self.resume_button.center_with_offset(0, 0, self.window.width, self.window.height, 0, -self.disconnect_button.get_height() - 5)


    def set_state(self, state: bool) -> None:
        """
        Set the screen's visibility/interactivity.
        """
        super().set_state(state)
        self.pause_label.set_state(state)
        self.resume_button.set_state(state)
        self.options_button.set_state(state)
        self.disconnect_button.set_state(state)
        if state: self.update_ui()
