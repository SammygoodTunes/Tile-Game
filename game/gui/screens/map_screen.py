"""
Module name: map_screen
"""

from __future__ import annotations

from pygame.draw import rect, line, circle
from pygame.surface import Surface
from pygame.transform import smoothscale_by
from typing import TYPE_CHECKING

if TYPE_CHECKING: from game.core.game import Game
from game.data.states.map_states import MapStates
from game.gui.screens.screen import Screen
from game.gui.label import Label
from game.network.builders.player_builder import PlayerBuilder


class MapScreen(Screen):
    """
    Class for creating the map screen.
    """

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self._got_map = False
        self.faded_surface = None
        self.title_label = Label('Map')
        self._map_data_copy: bytes = b''
        self.scaled_map: Surface = Surface((0, 0))

    def translate(self) -> None:
        pass

    def initialise_map(self) -> None:
        """
        Initialise the screen's map component.
        """
        _map = self.game.client.world.get_map()
        if self._got_map or _map.get_state()[0] != MapStates.READY or not self.game.start_game:
            return
        coefficient = min(self.game.width / _map.get_width_in_pixels() * 0.5,
                          self.game.height / _map.get_height_in_pixels() * 0.5)
        self.scaled_map = smoothscale_by(_map.get_surface(), round(coefficient, 2))
        self._got_map = True
        self.update_ui()

    def reset_map(self) -> None:
        """
        Reset the map attributes.
        """
        self._got_map = False

    def draw(self) -> None:
        if not self._enabled: return
        self.game.screen.blit(self.faded_surface, (0, 0))
        self.title_label.draw(self.game.screen)
        self.game.screen.blit(
            self.scaled_map,
            (self.game.width // 2 - self.scaled_map.get_width() // 2,
            self.game.height // 2 - self.scaled_map.get_height() // 2)
        )
        line(self.game.screen, (170, 170, 170),
             (
                self.game.width // 2 - self.scaled_map.get_width() // 2 + self.scaled_map.get_width() - 2,
                self.game.height // 2 - self.scaled_map.get_height() // 2
             ),
             (
                self.game.width // 2 - self.scaled_map.get_width() // 2 + self.scaled_map.get_width() - 2,
                self.game.height // 2 - self.scaled_map.get_height() // 2 + self.scaled_map.get_height()
             ), width=2)
        line(self.game.screen, (170, 170, 170),
             (
                self.game.width // 2 - self.scaled_map.get_width() // 2,
                self.game.height // 2 - self.scaled_map.get_height() // 2 + self.scaled_map.get_height() - 2
             ),
             (
                 self.game.width // 2 - self.scaled_map.get_width() // 2 + self.scaled_map.get_width(),
                 self.game.height // 2 - self.scaled_map.get_height() // 2 + self.scaled_map.get_height() - 2
             ), width=2)
        line(self.game.screen, (225, 225, 225),
             (
                 self.game.width // 2 - self.scaled_map.get_width() // 2,
                 self.game.height // 2 - self.scaled_map.get_height() // 2
             ),
             (
                 self.game.width // 2 - self.scaled_map.get_width() // 2,
                 self.game.height // 2 - self.scaled_map.get_height() // 2 + self.scaled_map.get_height()
             ), width=2)
        line(self.game.screen, (225, 225, 225),
             (
                 self.game.width // 2 - self.scaled_map.get_width() // 2,
                 self.game.height // 2 - self.scaled_map.get_height() // 2
             ),
             (
                 self.game.width // 2 - self.scaled_map.get_width() // 2 + self.scaled_map.get_width(),
                 self.game.height // 2 - self.scaled_map.get_height() // 2
             ), width=2)
        rect(self.game.screen, (0, 0, 0),
             (
                 self.game.width // 2 - self.scaled_map.get_width() // 2 - 2,
                 self.game.height // 2 - self.scaled_map.get_height() // 2 - 2,
                 self.scaled_map.get_width() + 4,
                 self.scaled_map.get_height() + 4
             ), width=2, border_radius=4)

        players = self.game.client.connection_handler.get_players()
        client_name = self.game.client.player.get_player_name()
        if len(players) > 1:
            index = self.game.client.connection_handler.get_player_index_by_name(client_name)
            players.append(players[index])
            players.pop(index)

        for player in players:
            is_client_player = player[PlayerBuilder.NAME_KEY] == client_name
            x, y = ((self.game.client.player.get_x(),
                    self.game.client.player.get_y())
                    if is_client_player else
                    (int(player[PlayerBuilder.X_POS_KEY]),
                    int(player[PlayerBuilder.Y_POS_KEY])))
            center_point = (
                self.game.width // 2 - self.scaled_map.get_width() // 2 + (
                        self.scaled_map.get_width() / self.game.client.world.get_map().get_width_in_pixels()
                        * (x + self.game.client.world.get_map().get_width_in_pixels() // 2
                        + self.game.client.player.width // 2)
                ),
                self.game.height // 2 - self.scaled_map.get_height() // 2 + (
                        self.scaled_map.get_height() / self.game.client.world.get_map().get_height_in_pixels()
                        * (y + self.game.client.world.get_map().get_height_in_pixels() // 2
                        + self.game.client.player.height // 2)
                )
            )

            circle(self.game.screen, (255 * is_client_player, 0, 255 * (not is_client_player)), center_point, 5)
            circle(self.game.screen, (255, 255, 255), center_point, 5, 2)
            circle(self.game.screen, (0, 0, 0), center_point, 6, 2)

    def update_ui(self) -> None:
        if not self._enabled: return
        map_data_copy = (
                self.game.client.world.get_map().get_dynatile_data()
                + int.to_bytes(self.game.width, length=4)
                + int.to_bytes(self.game.height, length=4)
        )
        if self._map_data_copy == map_data_copy:
            return
        if self._got_map:
            self._map_data_copy = map_data_copy
            coefficient = min(self.game.width / self.game.client.world.get_map().get_width_in_pixels() * 0.5,
                              self.game.height / self.game.client.world.get_map().get_height_in_pixels() * 0.5)
            self.scaled_map = smoothscale_by(self.game.client.world.get_map().get_surface(), round(coefficient, 2))

        self.faded_surface = self.initialise_surface()
        self.title_label.update(self.game)
        self.title_label.center_with_offset(0, 0, self.game.width, self.game.height, 0,
                                            -self.scaled_map.get_height() // 2 - self.title_label.get_height() - 5)

    def set_state(self, state: bool) -> None:
        super().set_state(state)
        self.title_label.set_state(state)
        if state: self.update_ui()
