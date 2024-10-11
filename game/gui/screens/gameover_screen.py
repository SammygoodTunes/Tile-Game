
from pygame import Surface

from game.data.properties.screen_properties import ScreenProperties
from game.gui.screens.screen import Screen
from game.gui.label import Label
from game.gui.button import Button
from game.utils.logger import logger


class GameoverScreen(Screen):
    """
    Class for creating the game-over screen.
    """

    def __init__(self, window) -> None:
        super().__init__()
        self.window = window
        self.faded_surface = self.initialise_surface()
        self.gameover_label = Label(text="You died.")
        self.respawn_button = Button(text="Respawn")
        self.disconnect_button = Button(text="Disconnect")

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
        self.gameover_label.draw(self.window.screen)
        self.respawn_button.draw(self.window.screen)
        self.disconnect_button.draw(self.window.screen)

    def update_ui(self) -> None:
        """
        Update the screen.
        """
        if not self._enabled:
            return
        self.faded_surface = self.initialise_surface()
        self.gameover_label.update(self.window)
        self.gameover_label.center_with_offset(0, 0, self.window.width, self.window.height, 0, -self.respawn_button.get_height() - 25 - self.gameover_label.get_total_height())
        self.respawn_button.update(self.window)
        self.respawn_button.center_with_offset(0, 0, self.window.width, self.window.height, 0, -self.disconnect_button.get_height() - 5)
        self.disconnect_button.update(self.window)
        self.disconnect_button.center_with_offset(0, 0, self.window.width, self.window.height, 0, 5)

    def set_state(self, state: bool) -> None:
        """
        Set the screen's visibility/interactivity.
        """
        super().set_state(state)
        self.gameover_label.set_state(state)
        self.respawn_button.set_state(state)
        self.disconnect_button.set_state(state)
        if state: self.update_ui()
