"""
Module name: serverconnect_screen
"""

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING: from game.core.game import Game
from game.data.states.connection_states import ConnectionStates
from game.gui.button import Button
from game.gui.label import Label
from game.gui.screens.screen import Screen


class ServerConnectScreen(Screen):
    """
    Class for creating the server connection screen.
    """

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self.faded_surface = None
        self.info_label = Label()
        self.main_menu_button = Button("Main menu")

    def translate(self) -> None:
        pass

    def draw(self) -> None:
        if not self._enabled:
            return
        self.game.screen.blit(self.faded_surface, (0, 0))
        self.info_label.draw(self.game.screen)
        self.main_menu_button.draw(self.game.screen)

    def update_ui(self) -> None:
        if not self._enabled:
            return
        self.faded_surface = self.initialise_surface()
        self.main_menu_button.resize(self.game)
        self.info_label.update(self.game)
        self.info_label.center_with_offset(0, 0, self.game.width, self.game.height, 0,
                                           -self.info_label.get_height() * 3)
        self.main_menu_button.center_with_offset(0, 0, self.game.width, self.game.height, 0,
                                                 self.main_menu_button.get_height())
        self.main_menu_button.update(self.game)

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
        super().set_state(state)
        self.info_label.set_state(state)
        self.main_menu_button.set_state(state)
        if state: self.update_ui()
