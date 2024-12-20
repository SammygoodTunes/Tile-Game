"""
Module name: credits_screen
"""

from __future__ import annotations
from pygame import MOUSEBUTTONUP
from pygame.event import Event
from typing import TYPE_CHECKING

if TYPE_CHECKING: from game.core.game import Game
from game.data.states.mouse_states import MouseStates
from game.gui.button import Button
from game.gui.label import Label
from game.gui.screens.screen import Screen


class CreditsScreen(Screen):
    """
    Class for creating the credits screen.
    """

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self.faded_surface = None
        self.options_label = Label('CREDITS')
        self.prog_title_label = Label('Programming by:')
        self.art_title_label = Label('Art by:')
        self.font_title_label = Label('Font by:')
        self.prog_value_label = Label('SammygoodTunes\nOnihilist').set_colour((255, 255, 0))
        self.art_value_label = Label('Pickmonde\nJatzylap\nSammygoodTunes').set_colour((255, 255, 0))
        self.font_value_label = Label('OmegaPC777').set_colour((255, 255, 0))
        self.back_button = Button("Back")

    def translate(self) -> None:
        pass

    def draw(self) -> None:
        if not self._enabled: return
        self.game.screen.blit(self.faded_surface, (0, 0))
        self.options_label.draw(self.game.screen)
        self.prog_title_label.draw(self.game.screen)
        self.prog_value_label.draw(self.game.screen)
        self.art_title_label.draw(self.game.screen)
        self.art_value_label.draw(self.game.screen)
        self.font_title_label.draw(self.game.screen)
        self.font_value_label.draw(self.game.screen)
        self.back_button.draw(self.game.screen)

    def update_ui(self) -> None:
        if not self._enabled: return
        self.faded_surface = self.initialise_surface()
        self.back_button.resize(self.game)
        self.options_label.update(self.game)
        self.prog_title_label.update(self.game)
        self.prog_value_label.update(self.game)
        self.art_title_label.update(self.game)
        self.art_value_label.update(self.game)
        self.font_title_label.update(self.game)
        self.font_value_label.update(self.game)
        y = -50 - 20 - self.options_label.get_height()
        self.options_label.center_with_offset(0, 0, self.game.width, self.game.height, 0, y)
        y += 10 + self.prog_title_label.get_height()
        self.prog_title_label.center_with_offset(0, 0, self.game.width, self.game.height, -self.prog_title_label.get_width() // 2 - 10, y)
        self.prog_value_label.center_with_offset(0, 0, self.game.width, self.game.height, self.prog_value_label.get_width() // 2 + 10, y)
        y += self.prog_value_label.get_total_height()
        self.art_title_label.center_with_offset(0, 0, self.game.width, self.game.height, -self.art_title_label.get_width() // 2 - 10, y)
        self.art_value_label.center_with_offset(0, 0, self.game.width, self.game.height, self.art_value_label.get_width() // 2 + 10, y)
        y += self.art_value_label.get_total_height()
        self.font_title_label.center_with_offset(0, 0, self.game.width, self.game.height, -self.font_title_label.get_width() // 2 - 10, y)
        self.font_value_label.center_with_offset(0, 0, self.game.width, self.game.height, self.font_value_label.get_width() // 2 + 10, y)
        y += 25 + self.font_value_label.get_total_height()
        self.back_button.center_with_offset(0, 0, self.game.width, self.game.height, 0, y)
        self.back_button.update(self.game)

    def set_state(self, state: bool) -> None:
        super().set_state(state)
        self.options_label.set_state(state)
        self.prog_title_label.set_state(state)
        self.prog_value_label.set_state(state)
        self.art_title_label.set_state(state)
        self.art_value_label.set_state(state)
        self.font_title_label.set_state(state)
        self.font_value_label.set_state(state)
        self.back_button.set_state(state)
        if state: self.update_ui()
