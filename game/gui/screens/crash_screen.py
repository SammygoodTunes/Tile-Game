"""
Module name: crash_screen
"""

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING: from game.core.game import Game
from game.gui.label import Label
from game.gui.screens.screen import Screen
from game.utils.translator import translator as t


class CrashScreen(Screen):
    """
    Class for creating the crash screen.
    """

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self.surface = None
        self.crash_label = Label(text="The game crashed")
        self.traceback_label = Label().set_colour((255, 50, 50)).set_shadow_colour((50, 0, 00))

    def translate(self) -> None:
        self.crash_label.set_text(t.t('screens.crash.crash_label'))

    def draw(self) -> None:
        if not self._enabled: return
        self.game.screen.blit(self.surface, (0, 0))
        self.traceback_label.draw(self.game.screen)
        self.crash_label.draw(self.game.screen)

    def update_ui(self) -> None:
        if not self._enabled: return
        self.crash_label.update(self.game)
        self.crash_label.set_y(24).center_horizontally(0, self.game.width)
        self.traceback_label.update(self.game)
        self.traceback_label.set_x(24).set_y(48)
        self.surface = self.initialise_surface()

    def set_state(self, state: bool) -> None:
        super().set_state(state)
        self.crash_label.set_state(state)
        self.traceback_label.set_state(state)
        if state: self.update_ui()
