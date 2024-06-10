
from pygame import Surface

from game.data.properties import ScreenProperties
from game.gui.screens.screen import Screen
from game.gui.label import Label
from game.gui.nametag import NameTag
from game.utils.logger import logger


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
        self._count = 0
        logger.debug(f'Created {__class__.__name__} with attributes {self.__dict__}')

    def draw(self) -> None:
        """
        Draw the screen and its components.
        """
        self.update_ui()
        if not self._enabled:
            return
        self.game.screen.blit(self._faded_surface, (self.game.width // 2 - self._faded_surface.get_width() // 2,
                                                    self.game.height // 2 - self._faded_surface.get_height() // 2))
        self.title_label.draw(self.game.screen)
        for nametag in self.player_list:
            nametag.draw(self.game.screen)

    def update_ui(self, bypass: bool = False) -> None:
        """
        Update the screen UI.
        """
        if self.game.client.connection_handler.connection is None:
            return
        players = self.game.client.connection_handler.connection.player_manager.players
        if self._count == len(players) and not bypass:
            return
        height = 0
        self._count = len(players)
        self.player_list = tuple()
        self.title_label.update(self.game)
        for player in players:
            nametag = (NameTag(player['name']).center_horizontally(0, self.game.width).set_state(True))
            nametag.set_y(height)
            nametag.update(self.game)
            height += nametag.get_height()
            self.player_list += (nametag,)
        self.title_label.center_horizontally(0, self.game.width)
        self._faded_surface = Surface((self.game.width // 2, height + self.title_label.get_total_height() + 10))
        self._faded_surface.fill((0, 0, 0))
        self._faded_surface.set_alpha(ScreenProperties.ALPHA)
        self.title_label.set_y(self.game.height // 2 - self._faded_surface.get_height() // 2)
        for i, nametag in enumerate(self.player_list):
            nametag.set_y(self.title_label.get_y() + self.title_label.get_total_height() + i * nametag.get_height())
            nametag.update(self.game)

    def set_state(self, state: bool) -> None:
        """
        Set the screen's visibility/interactivity.
        """
        super().set_state(state)
        self.title_label.set_state(state)
        for nametag in self.player_list:
            nametag.set_state(state)
