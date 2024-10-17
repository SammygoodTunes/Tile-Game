"""
Module name: serverconnect_screen
"""

from pygame import Surface

from game.data.properties.screen_properties import ScreenProperties
from game.data.states.connection_states import ConnectionStates
from game.gui.screens.screen import Screen
from game.gui.label import Label
from game.gui.button import Button


class ServerConnectScreen(Screen):
    """
    Class for creating the server connection screen.
    """

    def __init__(self, window) -> None:
        super().__init__()
        self.window = window
        self.faded_surface = self.initialise_surface()
        self.info_label = Label()
        self.main_menu_button = Button("Main menu")

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
        self.info_label.draw(self.window.screen)
        self.main_menu_button.draw(self.window.screen)

    def update_ui(self) -> None:
        """
        Update the screen UI.
        """
        if not self._enabled:
            return
        self.faded_surface = self.initialise_surface()
        self.info_label.update(self.window)
        self.info_label.center_with_offset(0, 0, self.window.width, self.window.height, 0,
                                           -self.info_label.get_total_height() * 3)
        self.main_menu_button.update(self.window)
        self.main_menu_button.center_with_offset(0, 0, self.window.width, self.window.height, 0,
                                                 self.main_menu_button.get_height())

    def update_info_label(self, code: int) -> None:
        """
        Update info label's text and colour based on received connection code, then update the screen UI.
        """
        if code == ConnectionStates.SUCCESS:
            self.info_label.set_text('Connection successful.').set_colour((0, 255, 0))
        elif code == ConnectionStates.INVALID:
            self.info_label.set_text('Unknown host.').set_colour((255, 0, 0))
        elif code == ConnectionStates.REFUSED:
            self.info_label.set_text('Failed to connect to server.').set_colour((255, 0, 0))
        elif code == ConnectionStates.TIMEOUT:
            self.info_label.set_text('Connection timed out.').set_colour((255, 0, 0))
        elif code == ConnectionStates.NOROUTE:
            self.info_label.set_text('No route to host.').set_colour((255, 0, 0))
        elif code == ConnectionStates.DISCONNECTED:
            self.info_label.set_text('Disconnected.').set_colour((255, 0, 0))
        elif code == ConnectionStates.BADNAME:
            self.info_label.set_text('Player name is already taken.').set_colour((255, 0, 0))
        elif code == ConnectionStates.MAXIMUM:
            self.info_label.set_text('Server is full. Come back later!').set_colour((255, 0, 0))
        elif code == ConnectionStates.ERROR:
            self.info_label.set_text('An internal error has occurred.').set_colour((255, 0, 0))
        elif code == ConnectionStates.SERVFAIL:
            self.info_label.set_text('A server is already running on this machine.').set_colour((255, 0, 0))
        elif code == ConnectionStates.GETDATA:
            self.info_label.set_text('Loading world...').set_colour((255, 255, 0))
        else:
            self.info_label.set_text('Connecting to server...').set_colour((255, 255, 0))
        self.main_menu_button.set_state(code >= 0)
        self.update_ui()

    def reset_info_label(self) -> None:
        """
        Reset the information label back to its default state, then update the screen UI.
        """
        self.info_label.set_text('Connecting to server...').set_colour((255, 255, 0))
        self.update_ui()

    def set_state(self, state: bool) -> None:
        """
        Set the screen's visibility/interactivity.
        """
        super().set_state(state)
        self.info_label.set_state(state)
        self.main_menu_button.set_state(state)
        if state: self.update_ui()
