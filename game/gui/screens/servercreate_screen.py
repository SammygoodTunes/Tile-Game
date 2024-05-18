
from pygame import Surface
from pygame.event import Event

import game.data.data_manager as data_mng
from game.data.properties import ScreenProperties, PlayerProperties
from game.gui.screens.screen import Screen
from game.gui.label import Label
from game.gui.button import Button
from game.gui.inputbox import InputBox
from game.utils.logger import logger


class ServerCreateScreen(Screen):
    """
    Class for creating the server create screen.
    """

    def __init__(self, window) -> None:
        super().__init__()
        self.window = window
        self.faded_surface = self.initialise_surface()
        self.create_label = Label("Create server")
        self.ign_input = (InputBox(placeholder='Player name').
                          set_max_text_length(PlayerProperties.MAX_PLAYER_NAME_SIZE).authorise_only_alnum())
        self.create_button = Button('Create')
        self.back_button = Button('Back')
        logger.debug(f'Created {__class__.__name__} with attributes {self.__dict__}')

    def initialise_surface(self) -> Surface:
        """
        Initialise the screen's surface.
        """
        surface = Surface((self.window.width, self.window.height))
        surface.fill((0, 0, 0))
        surface.set_alpha(ScreenProperties.ALPHA)
        return surface

    def events(self, e: Event) -> None:
        """
        Track the screen events (unused).
        """
        self.ign_input.events(e)
        self.create_button.set_state(
            bool(self.ign_input.get_text().strip())
        )

    def draw(self) -> None:
        """
        Draw the screen and its components.
        """
        if not self._enabled:
            return
        self.window.screen.blit(self.faded_surface, (0, 0))
        self.create_label.draw(self.window.screen)
        self.ign_input.draw(self.window.screen)
        self.create_button.draw(self.window.screen)
        self.back_button.draw(self.window.screen)

    def update_ui(self) -> None:
        """
        Update the screen UI.
        """
        self.faded_surface = self.initialise_surface()
        self.create_label.update(self.window)
        self.create_label.center_with_offset(0, 0, self.window.width, self.window.height, 0, -self.create_label.get_total_height() * 3)
        self.ign_input.update(self.window)
        self.ign_input.center_with_offset(0, 0, self.window.width, self.window.height, 0, -10)
        self.create_button.update(self.window)
        self.create_button.center_with_offset(0, 0, self.window.width, self.window.height, 0, self.ign_input.get_height() + 15)
        self.back_button.update(self.window)
        self.back_button.center_with_offset(0, 0, self.window.width, self.window.height, 0,  self.ign_input.get_height() + self.create_button.get_height() + 20)
        self.create_button.set_state(bool(self.ign_input.get_text().strip()))

    def set_state(self, state: bool) -> None:
        """
        Set the screen's visibility/interactivity.
        """
        super().set_state(state)
        self.create_label.set_state(state)
        self.ign_input.set_state(state)
        self.create_button.set_state(state)
        self.back_button.set_state(state)
