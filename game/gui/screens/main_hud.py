"""
Module name: main_hud
"""

from __future__ import annotations
from time import time
from typing import TYPE_CHECKING

if TYPE_CHECKING: from game.core.game import Game
from game.data.properties.game_properties import GameProperties
from game.gui.hotbar import Hotbar
from game.gui.label import Label
from game.gui.progress_bar import ProgressBar
from game.gui.screens.screen import Screen
from game.utils.translator import translator as t


class MainHud(Screen):
    """
    Class for creating the main (player) HUD.
    """

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self.surface = None
        self.version_label = (Label(f'v{GameProperties.APP_VER}')
                              .set_font_sizes((8, 10, 12))
                              .set_colour((255, 255, 10))
                              .set_x(4))
        self.score_label = Label()
        self.ping_label = Label()
        self.data_sent_label = Label()
        self.data_recv_label = Label()
        self.data_sent_rate_label = Label()
        self.data_recv_rate_label = Label()
        self.camera_label = Label()
        self.position_label = Label()
        self.health_bar = (ProgressBar(title="Player health")
                           .set_filled_end_colour((20, 131, 240))
                           .set_state(True))
        self.hotbar = Hotbar(slot_count=6).select_slot(0)
        self.timer = time()

    def translate(self) -> None:
        self.health_bar.info_label.set_text(t.t('screens.hud.health_bar_label'))

    def draw(self) -> None:
        if not self._enabled: return
        c_handler = self.game.client.connection_handler
        self.score_label.set_text(f'Score: {self.game.client.player.score}')
        self.score_label.draw(self.game.screen)
        self.health_bar.draw(self.game.screen)
        self.hotbar.draw(self.game.screen)
        self.version_label.draw(self.game.screen)

        self.health_bar.update(self.game)

        if not self.game.screens.options_screen.debug_info_box.is_checked():
            return

        self.data_sent_label.set_text(f'Data sent: {c_handler.get_total_data_sent():.3f} MB')
        self.data_recv_label.set_text(f'Data received: {c_handler.get_total_data_received():.3f} MB')
        self.camera_label.set_text(f'Camera (XY): {self.game.client.camera.x: .0f} {self.game.client.camera.y: .0f}')
        self.position_label.set_text(
            f'Player (XY): {self.game.client.player.get_x(): .0f} {self.game.client.player.get_y(): .0f}')
        self.ping_label.set_x(self.game.width - self.ping_label.get_width() - 2)
        self.ping_label.set_y(-8 + self.score_label.get_height() // 2 + 4)
        self.data_sent_label.set_x(self.game.width - self.data_sent_label.get_width() - 2)
        self.data_sent_label.set_y(self.ping_label.get_y() + self.ping_label.get_height() // 2 + 2)
        self.data_recv_label.set_x(self.game.width - self.data_recv_label.get_width() - 2)
        self.data_recv_label.set_y(self.data_sent_label.get_y() + self.data_sent_label.get_height() // 2 + 2)
        self.data_sent_rate_label.set_x(self.game.width - self.data_sent_rate_label.get_width() - 2)
        self.data_sent_rate_label.set_y(self.data_recv_label.get_y() + self.data_recv_label.get_height() // 2 + 2)
        self.data_recv_rate_label.set_x(self.game.width - self.data_recv_rate_label.get_width() - 2)
        self.data_recv_rate_label.set_y(self.data_sent_rate_label.get_y() + self.data_sent_rate_label.get_height() // 2 + 2)

        self.ping_label.draw(self.game.screen)
        self.data_sent_label.draw(self.game.screen)
        self.data_recv_label.draw(self.game.screen)
        self.data_sent_rate_label.draw(self.game.screen)
        self.data_recv_rate_label.draw(self.game.screen)
        self.camera_label.draw(self.game.screen)
        self.position_label.draw(self.game.screen)

        if not time() - self.timer > 1.0:
            return
        self.ping_label.set_text(f'Ping: {c_handler.get_ping()} (ms)')
        self.data_sent_rate_label.set_text(
            f'Data transmission rate: {c_handler.get_average_data_sent():.1f} KB/min'
        )
        self.data_recv_rate_label.set_text(
            f'Data reception rate: {c_handler.get_average_data_received():.1f} KB/min'
        )
        self.timer = time()

    def update_ui(self) -> None:
        if not self._enabled: return
        self.surface = self.initialise_surface(alpha=0)
        y: int = -8
        self.health_bar.resize(self.game)
        self.hotbar.update(self.game)
        self.score_label.update(self.game)
        self.ping_label.update(self.game)
        self.data_sent_label.update(self.game)
        self.data_recv_label.update(self.game)
        self.data_sent_rate_label.update(self.game)
        self.data_recv_rate_label.update(self.game)
        self.camera_label.update(self.game)
        self.position_label.update(self.game)
        self.version_label.update(self.game)
        self.health_bar.set_y(self.health_bar.get_height()).center_horizontally(0, self.game.width)
        self.hotbar.set_y(self.game.height - self.hotbar.get_height() - 16).center_horizontally(0, self.game.width)
        self.score_label.set_x(4)
        self.score_label.set_y(y)
        y += self.score_label.get_font_size() + 4
        self.camera_label.set_x(4)
        self.camera_label.set_y(y)
        y += self.camera_label.get_font_size() + 4
        self.position_label.set_x(4)
        self.position_label.set_y(y)
        self.version_label.set_y(self.game.height - self.version_label.get_height())
        self.health_bar.update(self.game)

    def set_state(self, state: bool) -> None:
        super().set_state(state)
        self.score_label.set_state(state)
        self.ping_label.set_state(state)
        self.data_sent_label.set_state(state)
        self.data_recv_label.set_state(state)
        self.data_sent_rate_label.set_state(state)
        self.data_recv_rate_label.set_state(state)
        self.camera_label.set_state(state)
        self.position_label.set_state(state)
        self.version_label.set_state(state)
        self.health_bar.set_state(state)
        self.hotbar.set_state(state)
        if state: self.update_ui()
