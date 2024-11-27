"""
Module name: mainmenu_screen
"""

from __future__ import annotations
from numpy import exp, cos, pi, absolute
from typing import TYPE_CHECKING
import pygame.time

if TYPE_CHECKING: from game.core.game import Game
from game.data.properties.game_properties import GameProperties
from game.data.properties.gui_properties import GuiProperties
from game.gui.button import Button
from game.gui.label import Label
from game.gui.screens.screen import Screen
from game.utils.translator import translator as t

class MainMenuScreen(Screen):
    """
    Class for creating the main menu screen.
    """

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self.title_label = (Label(GameProperties.APP_NAME)
                            .set_font_sizes((15, 30, 50))
                            .set_colour((200, 200, 255)))
        self.version_label = (Label(f'v{GameProperties.APP_VER}')
                              .set_font_sizes((8, 10, 12))
                              .set_colour((255, 255, 10)))
        self.play_button = Button("Play")
        self.options_button = Button("Options")
        self.credits_button = Button("Credits")
        self.quit_button = Button("Quit")
        self.title_label_time: float = pygame.time.get_ticks() / 1000.0
        self.set_state(True)

    def translate(self) -> None:
        self.play_button.set_text(t.t('screens.mainmenu.play_button'))
        self.options_button.set_text(t.t('screens.mainmenu.options_button'))
        self.credits_button.set_text(t.t('screens.mainmenu.credits_button'))
        self.quit_button.set_text(t.t('screens.mainmenu.quit_button'))

    def draw(self) -> None:
        if not self._enabled: return
        label_time = pygame.time.get_ticks() / 1000.0 - self.title_label_time
        if label_time > GuiProperties.TITLE_ANIM_DURATION:
            label_time = GuiProperties.TITLE_ANIM_DURATION

        self.title_label.center_with_offset(
            0,
            0,
            self.game.width,
            self.game.height,
            0,
            -self.title_label.get_height() - (
                    absolute(exp(-label_time * 3) * cos(pi * label_time * 3)) * 250
            )
        )
        self.title_label.draw(self.game.screen)
        self.version_label.draw(self.game.screen)
        self.play_button.draw(self.game.screen)
        self.options_button.draw(self.game.screen)
        self.credits_button.draw(self.game.screen)
        self.quit_button.draw(self.game.screen)

    def update_ui(self) -> None:
        if not self._enabled: return
        self.play_button.resize(self.game)
        self.options_button.resize(self.game)
        self.credits_button.resize(self.game)
        self.quit_button.resize(self.game)

        self.title_label.update(self.game)
        self.version_label.update(self.game)

        self.version_label.set_x(4).set_y(self.game.height - self.version_label.get_height())
        self.play_button.center(0, 0, self.game.width, self.game.height)
        self.options_button.center_with_offset(
            0,
            0,
            self.game.width,
            self.game.height,
            0,
            self.play_button.get_height() + 5
        )
        self.credits_button.center_with_offset(
            0,
            0,
            self.game.width,
            self.game.height,
            0,
            self.play_button.get_height() + self.options_button.get_height() + 10
        )
        self.quit_button.center_with_offset(
            0,
            0,
            self.game.width,
            self.game.height,
            0,
            self.play_button.get_height() + self.options_button.get_height() + self.credits_button.get_height() + 15
        )

        self.play_button.update(self.game)
        self.options_button.update(self.game)
        self.credits_button.update(self.game)
        self.quit_button.update(self.game)

    def set_state(self, state: bool) -> None:
        super().set_state(state)
        self.title_label.set_state(state)
        self.version_label.set_state(state)
        self.play_button.set_state(state)
        self.options_button.set_state(state)
        self.credits_button.set_state(state)
        self.quit_button.set_state(state)
        self.title_label_time: float = pygame.time.get_ticks() / 1000.0
        if state: self.update_ui()
