"""
Module name: playerlist_screen
"""

from __future__ import annotations
from pygame import Surface
from typing import TYPE_CHECKING

if TYPE_CHECKING: from game.core.game import Game
from game.data.properties.screen_properties import ScreenProperties
from game.data.properties.server_properties import ServerProperties
from game.gui.label import Label
from game.gui.nametag import NameTag
from game.gui.screens.screen import Screen
from game.utils.translator import translator as t


class PlayerListScreen(Screen):
    """
    Class for creating the player list screen.
    """

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self.title_label = Label('Player list')
        self.player_list: tuple[NameTag] = tuple()
        self._faded_surface: Surface = Surface((0, 0))
        self._playercount_surface: Surface = Surface((0, 0))
        self._update_buffer: bytes = b''
        self.count_label = Label('ONLINE   0/10').set_font_sizes((7, 8, 9)).set_colour((0, 255, 0))

    def translate(self) -> None:
        self.title_label.set_text(t.t('screens.playerlist.title_label'))

    def draw(self) -> None:
        if not self._enabled: return
        self.game.screen.blit(self._faded_surface, (
            self.game.width / 2 - self._faded_surface.get_width() / 2,
            self.game.height / 2 - self._faded_surface.get_height() / 2
        ))
        self.game.screen.blit(self._playercount_surface, (
            self.game.width / 2 + self._faded_surface.get_width() / 2 - self._playercount_surface.get_width(),
            self.game.height / 2 - self._faded_surface.get_height() / 2 - self._playercount_surface.get_height()
        ))
        self.title_label.draw(self.game.screen)
        self.count_label.draw(self.game.screen)
        for nametag in self.player_list:
            nametag.draw(self.game.screen)

    def update_ui(self) -> None:
        if not self._enabled or self.game.client.connection_handler.connection is None: return
        players = self.game.client.connection_handler.connection.player_manager.players
        update_buffer = (
                int.to_bytes(len(players))
                + int.to_bytes(self.game.width, length=4)
                + int.to_bytes(self.game.height, length=4)
        )
        if update_buffer == self._update_buffer:
            return
        height = 0
        self._update_buffer = update_buffer
        self.player_list = tuple()
        self.count_label.set_text(f'{t.t("screens.playerlist.online_text")}   {len(players)}/{ServerProperties.MAX_PLAYERS}')
        self.title_label.update(self.game)
        self.count_label.update(self.game)
        for player in players:
            nametag = (NameTag(player['name']).set_state(True))
            nametag.resize(self.game)
            nametag.set_y(height)
            nametag.update(self.game)
            nametag.center_horizontally(0, self.game.width)
            height += nametag.get_height()
            self.player_list += nametag,
        self._faded_surface = Surface((self.game.width / 2, height + self.title_label.get_height() + 10))
        self._faded_surface.fill((0, 0, 0))
        self._faded_surface.set_alpha(ScreenProperties.ALPHA)
        self._playercount_surface = Surface((self.count_label.get_width() + 10, self.count_label.get_height() + 5))
        self._playercount_surface.fill((0, 0, 0))
        self._playercount_surface.set_alpha(ScreenProperties.PRONOUNCED_ALPHA)
        self.title_label.center_horizontally(0, self.game.width)
        self.count_label.center_horizontally(
            self.game.width // 2 + self._faded_surface.get_width() // 2 - self._playercount_surface.get_width(),
            self._playercount_surface.get_width()
        )
        self.count_label.center_vertically(
            self.game.height // 2 - self._faded_surface.get_height() // 2 - self._playercount_surface.get_height(),
            self._playercount_surface.get_height()
        )
        self.title_label.set_y(self.game.height // 2 - self._faded_surface.get_height() // 2)
        for i, nametag in enumerate(self.player_list):
            nametag.resize(self.game)
            nametag.set_y(self.title_label.get_y() + self.title_label.get_height() + i * nametag.get_height())
            nametag.update(self.game)

    def set_state(self, state: bool) -> None:
        super().set_state(state)
        self.title_label.set_state(state)
        self.count_label.set_state(state)
        for nametag in self.player_list:
            nametag.set_state(state)
        if state: self.update_ui()
