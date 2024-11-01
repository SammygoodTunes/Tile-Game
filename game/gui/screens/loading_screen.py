"""
Module name: loading_screen
"""

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING: from game.core.game import Game
from game.gui.progress_bar import ProgressBar
from game.gui.screens.screen import Screen


class LoadingScreen(Screen):
    """
    Class for creating the loading screen.
    """

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self.surface = None
        self.progress_bar = ProgressBar()

    def draw(self) -> None:
        if not self._enabled: return
        self.game.screen.blit(self.surface, (0, 0))
        self.progress_bar.draw(self.game.screen)

    def update_ui(self) -> None:
        if not self._enabled: return
        self.surface = self.initialise_surface()
        self.progress_bar.update(self.game)
        self.progress_bar.center(0, 0, self.game.width, self.game.height)

    def set_state(self, state: bool) -> None:
        super().set_state(state)
        self.progress_bar.set_state(state)
        if state: self.update_ui()
