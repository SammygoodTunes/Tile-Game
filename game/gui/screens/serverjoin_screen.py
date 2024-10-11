from pygame import Surface
from pygame.event import Event

from game.data.properties.player_properties import PlayerProperties
from game.data.properties.screen_properties import ScreenProperties
from game.gui.screens.screen import Screen
from game.gui.label import Label
from game.gui.button import Button
from game.gui.inputbox import InputBox


class ServerJoinScreen(Screen):
    """
    Class for creating the server join screen.
    """

    def __init__(self, window) -> None:
        super().__init__()
        self.window = window
        self.faded_surface = self.initialise_surface()
        self.join_label = Label("Join server")
        self.ign_input = (InputBox(placeholder='Player name')
                          .set_max_text_length(PlayerProperties.MAX_PLAYER_NAME_SIZE).authorise_only_alnumlines())
        self.ip_input = InputBox(placeholder='IP address').set_max_text_length(32)
        self.port_input = InputBox(placeholder='Port').set_max_text_length(5).authorise_only_numeric()
        self.join_button = Button('Join')
        self.back_button = Button('Back')

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
        self.ip_input.events(e)
        self.port_input.events(e)
        self.join_button.set_state(
            self.ign_input.get_text().strip()
            and self.ip_input.get_text().strip()
            and self.port_input.get_text().strip()
        )

    def draw(self) -> None:
        """
        Draw the screen and its components.
        """
        if not self._enabled:
            return
        self.window.screen.blit(self.faded_surface, (0, 0))
        self.join_label.draw(self.window.screen)
        self.ign_input.draw(self.window.screen)
        self.ip_input.draw(self.window.screen)
        self.port_input.draw(self.window.screen)
        self.join_button.draw(self.window.screen)
        self.back_button.draw(self.window.screen)

    def update_ui(self) -> None:
        """
        Update the screen UI.
        """
        if not self._enabled:
            return
        self.faded_surface = self.initialise_surface()
        self.join_label.update(self.window)
        self.join_label.center_with_offset(0, 0, self.window.width, self.window.height, 0,
                                           -self.ip_input.get_height() - self.join_label.get_total_height() * 3)
        self.ign_input.update(self.window)
        self.ign_input.center_with_offset(0, 0, self.window.width, self.window.height, 0,
                                          -self.ign_input.get_height() - 10)
        self.ip_input.update(self.window)
        self.ip_input.center_with_offset(0, 0, self.window.width, self.window.height, 0, -5)
        self.port_input.update(self.window)
        self.port_input.center_with_offset(0, 0, self.window.width, self.window.height, 0, self.ip_input.get_height())
        self.join_button.update(self.window)
        self.join_button.center_with_offset(0, 0, self.window.width, self.window.height, 0,
                                            self.ip_input.get_height() + self.port_input.get_height() + 15)
        self.back_button.update(self.window)
        self.back_button.center_with_offset(0, 0, self.window.width, self.window.height, 0,
                                            self.ip_input.get_height() + self.port_input.get_height() + self.join_button.get_height() + 20)
        self.join_button.set_state(
            self.ign_input.get_text().strip()
            and self.ip_input.get_text().strip()
            and self.port_input.get_text().strip()
        )

    def set_state(self, state: bool) -> None:
        """
        Set the screen's visibility/interactivity.
        """
        super().set_state(state)
        self.join_label.set_state(state)
        self.ign_input.set_state(state)
        self.ip_input.set_state(state)
        self.port_input.set_state(state)
        self.join_button.set_state(state)
        self.back_button.set_state(state)
        if state: self.update_ui()
