
from pygame import Surface

from game.data.properties.screen_properties import ScreenProperties
from game.data.properties.server_properties import ServerProperties
from game.gui.screens.screen import Screen
from game.gui.label import Label
from game.gui.nametag import NameTag


class PlayerListScreen(Screen):
    """
    Class for creating the player list screen.
    """

    def __init__(self, game) -> None:
        super().__init__()
        self.game = game
        self.title_label = Label('Player list')
        self.player_list: tuple[NameTag] = tuple()
        self._faded_surface: Surface = Surface((0, 0))
        self._playercount_surface: Surface = Surface((0, 0))
        self.count_label = Label('ONLINE   0/10').set_font_sizes((7, 8, 9)).set_colour((0, 255, 0))

    def draw(self) -> None:
        """
        Draw the screen and its components.
        """
        self.update_ui()
        if not self._enabled:
            return
        self.game.screen.blit(self._faded_surface, (self.game.width / 2 - self._faded_surface.get_width() / 2,
                                                    self.game.height / 2 - self._faded_surface.get_height() / 2))
        self.game.screen.blit(self._playercount_surface, (self.game.width / 2 + self._faded_surface.get_width() / 2 - self._playercount_surface.get_width(),
                                                          self.game.height / 2 - self._faded_surface.get_height() / 2 - self._playercount_surface.get_height()))
        self.title_label.draw(self.game.screen)
        self.count_label.draw(self.game.screen)
        for nametag in self.player_list:
            nametag.draw(self.game.screen)

    def update_ui(self) -> None:
        """
        Update the screen UI.
        """
        if not self._enabled or self.game.client.connection_handler.connection is None:
            return
        players = self.game.client.connection_handler.connection.player_manager.players
        height = 0
        self.player_list = tuple()
        self.count_label.set_text(f'ONLINE   {len(players)}/{ServerProperties.MAX_PLAYERS}')
        self.title_label.update(self.game)
        self.count_label.update(self.game)
        for player in players:
            nametag = (NameTag(player['name']).center_horizontally(0, self.game.width).set_state(True))
            nametag.set_y(height)
            nametag.update(self.game)
            height += nametag.get_height()
            self.player_list += (nametag,)
        self.title_label.center_horizontally(0, self.game.width)
        self.count_label.center_horizontally(
            self.game.width / 2 + self._faded_surface.get_width() / 2 - self._playercount_surface.get_width(),
            self._playercount_surface.get_width()
        )
        self.count_label.center_vertically(
            self.game.height / 2 - self._faded_surface.get_height() / 2 - self._playercount_surface.get_height(),
            self._playercount_surface.get_height()
        )
        self._faded_surface = Surface((self.game.width / 2, height + self.title_label.get_total_height() + 10))
        self._faded_surface.fill((0, 0, 0))
        self._faded_surface.set_alpha(ScreenProperties.ALPHA)
        self._playercount_surface = Surface((self.count_label.get_total_width() + 10, self.count_label.get_total_height() + 5))
        self._playercount_surface.fill((0, 0, 0))
        self._playercount_surface.set_alpha(ScreenProperties.PRONOUNCED_ALPHA)
        self.title_label.set_y(self.game.height / 2 - self._faded_surface.get_height() / 2)
        for i, nametag in enumerate(self.player_list):
            nametag.set_y(self.title_label.get_y() + self.title_label.get_total_height() + i * nametag.get_height())
            nametag.update(self.game)

    def set_state(self, state: bool) -> None:
        """
        Set the screen's visibility/interactivity.
        """
        super().set_state(state)
        self.title_label.set_state(state)
        self.count_label.set_state(state)
        for nametag in self.player_list:
            nametag.set_state(state)
        if state: self.update_ui()
