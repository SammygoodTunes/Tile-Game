
from __future__ import annotations
from datetime import date
from math import sin
from pygame import Surface, time, draw
from typing import TYPE_CHECKING

if TYPE_CHECKING: from game.core.game import Game
from game.gui.screens.screen import Screen
from game.data.properties.gui_properties import GuiProperties


class FxScreen(Screen):
    """
    Class for creating an effect layer screen.
    """

    def __init__(self, game: Game) -> None:
        super().__init__(game)

    @staticmethod
    def draw_falling_snow_layer(screen: Surface):
        """
        Draw falling snow layer to screen.
        """
        if not date(date.today().year - 1, 12, 20) <= date.today() <= date(date.today().year, 1, 20):
            return
        for i in range(GuiProperties.SNOW_PARTICLE_DENSITY[0]):
            for j in range(GuiProperties.SNOW_PARTICLE_DENSITY[1]):
                draw.rect(screen, (255, 255, 255), (
                    (sin(time.get_ticks() / 1000.0) * 100.0 + j * screen.get_width() / 3 + i * screen.get_width() / 7) % (screen.get_width() + 4),
                    (time.get_ticks() / 15.0 + i * screen.get_height() / 3 + j * screen.get_height() / 5) % (screen.get_height() + 4),
                    4,
                    4
                ))
                draw.rect(screen, (200, 200, 200), (
                    (sin(time.get_ticks() / 900.0) * 70.0 + j * screen.get_width() / 3 + i * screen.get_width() / 7) % (screen.get_width() + 2),
                    (time.get_ticks() / 20.0 + i * screen.get_height() / 3 + j * screen.get_height() / 5) % (screen.get_height() + 2),
                    2,
                    2
                ))
                draw.rect(screen, (150, 150, 150), (
                    (sin(time.get_ticks() / 1000.0) * 50.0 + j * screen.get_width() / 3 + i * screen.get_width() / 7) % (screen.get_width() + 1),
                    (time.get_ticks() / 25.0 + i * screen.get_height() / 3 + j * screen.get_height() / 5) % (screen.get_height() + 1),
                    1,
                    1
                ))

