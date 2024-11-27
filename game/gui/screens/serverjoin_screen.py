"""
Module name: serverjoin_screen
"""

from __future__ import annotations
from pygame.event import Event
from typing import TYPE_CHECKING

if TYPE_CHECKING: from game.core.game import Game
from game.data.properties.player_properties import PlayerProperties
from game.gui.button import Button
from game.gui.inputbox import InputBox
from game.gui.label import Label
from game.gui.ordering_container import OrderingContainer
from game.gui.screens.screen import Screen
from game.utils.translator import translator as t


class ServerJoinScreen(Screen):
    """
    Class for creating the server join screen.
    """

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self.faded_surface = None
        self.join_label = Label("Join server")
        self.ign_input = (InputBox(placeholder_text='Player name', tooltip_text='Player name')
                          .set_max_text_length(PlayerProperties.MAX_PLAYER_NAME_SIZE)
                          .authorise_only_alnumlines())
        self.ip_input = (InputBox(placeholder_text='IP address', tooltip_text='IP address')
                         .set_max_text_length(32)
                         .authorise_only_alnumdot())
        self.port_input = (InputBox(placeholder_text='Port', tooltip_text='Port')
                           .set_max_text_length(5)
                           .authorise_only_numeric())
        self.join_button = Button('Join')
        self.back_button = Button('Back')
        self.ordering_container = OrderingContainer().set_widgets([
            self.ign_input,
            self.ip_input,
            self.port_input
        ])

    def events(self, e: Event) -> None:
        if not self._enabled: return
        self.ign_input.events(e)
        self.ip_input.events(e)
        self.port_input.events(e)
        self.join_button.set_state(bool(
            self.ign_input.get_text().strip()
            and self.ip_input.get_text().strip()
            and self.port_input.get_text().strip()
        ))
        self.ordering_container.events(e)

    def translate(self) -> None:
        self.join_label.set_text(t.t('screens.serverjoin.join_label'))
        self.ign_input.set_text(t.t('screens.serverjoin.ign_input'))
        self.ip_input.set_text(t.t('screens.serverjoin.ip_input'))
        self.port_input.set_text(t.t('screens.serverjoin.port_input'))
        self.join_button.label.set_text(t.t('screens.serverjoin.join_button'))
        self.back_button.label.set_text(t.t('screens.serverjoin.back_button'))

    def draw(self) -> None:
        if not self._enabled: return
        self.game.screen.blit(self.faded_surface, (0, 0))
        self.join_label.draw(self.game.screen)
        for inputbox in self.ordering_container.get_widgets():
            if isinstance(inputbox, InputBox):
                inputbox.draw(self.game.screen)
        self.join_button.draw(self.game.screen)
        self.back_button.draw(self.game.screen)

    def update_ui(self) -> None:
        if not self._enabled: return
        self.faded_surface = self.initialise_surface()
        self.join_button.resize(self.game)
        self.back_button.resize(self.game)
        self.join_label.update(self.game)
        self.join_label.center_with_offset(
            0,
            0,
            self.game.width,
            self.game.height,
            0,
            -self.ip_input.get_height() - self.join_label.get_height() - 30
        )
        self.ign_input.center_with_offset(
            0,
            0,
            self.game.width,
            self.game.height,
            0,
            -self.ign_input.get_height() - 10
        )
        self.ip_input.center_with_offset(0, 0, self.game.width, self.game.height, 0, -5)
        self.port_input.center_with_offset(0, 0, self.game.width, self.game.height, 0, self.ip_input.get_height())
        self.join_button.center_with_offset(
            0,
            0,
            self.game.width,
            self.game.height,
            0,
            self.ip_input.get_height() + self.port_input.get_height() + 10
        )
        self.back_button.center_with_offset(
            0,
            0,
            self.game.width,
            self.game.height,
            0,
            self.ip_input.get_height() + self.port_input.get_height() + self.join_button.get_height() + 15
        )
        self.ign_input.update(self.game)
        self.ip_input.update(self.game)
        self.port_input.update(self.game)
        self.join_button.update(self.game)
        self.back_button.update(self.game)
        self.join_button.set_state(bool(
            self.ign_input.get_text().strip()
            and self.ip_input.get_text().strip()
            and self.port_input.get_text().strip()
        ))

    def set_state(self, state: bool) -> None:
        super().set_state(state)
        self.join_label.set_state(state)
        self.ign_input.set_state(state)
        self.ip_input.set_state(state)
        self.port_input.set_state(state)
        self.join_button.set_state(state)
        self.back_button.set_state(state)
        self.ordering_container.set_state(state)
        if state: self.update_ui()
        else:
            self.ign_input.set_selected(state)
            self.ip_input.set_selected(state)
            self.port_input.set_selected(state)
