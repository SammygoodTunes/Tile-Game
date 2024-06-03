
from pygame.surface import Surface

from game.data.data_manager import get_game_property, APP_VERSION
from game.gui.hotbar import Hotbar
from game.gui.label import Label
from game.gui.progress_bar import ProgressBar
from game.gui.screens.screen import Screen
from game.utils.logger import logger


class MainHud(Screen):
    """
    Class for creating the main (player) HUD.
    """

    def __init__(self, game) -> None:
        super().__init__()
        self.game = game
        self.surface = Surface((self.game.width, self.game.height))
        self.version_label = Label(f'v{get_game_property(APP_VERSION).strip()}').set_font_sizes(
            (8, 10, 12)).set_colour((255, 255, 10))
        self.score_label = Label()
        self.camera_label = Label()
        self.position_label = Label()
        self.health_bar = ProgressBar(title="Player health").set_value(self.game.player.get_health()).set_state(True)
        self.hotbar = Hotbar(slot_count=6).select_slot(0)
        logger.debug(f'Created {__class__.__name__} with attributes {self.__dict__}')

    def draw(self) -> None:
        """
        Draw the screen and its components.
        """
        if self._enabled:
            if self.game.screens.options_screen.debug_info_box.is_checked():
                self.camera_label.set_text(f"Camera (XY): {self.game.camera.x: .0f} {self.game.camera.y: .0f}")
                self.position_label.set_text(
                    f"Player (XY): {self.game.player.get_x(): .0f} {self.game.player.get_y(): .0f}")
                self.camera_label.draw(self.game.screen)
                self.position_label.draw(self.game.screen)
            self.score_label.set_text(f"Score: {self.game.player.score}")
            self.score_label.draw(self.game.screen)
            self.health_bar.draw(self.game.screen)
            self.hotbar.draw(self.game.screen)

    def update_ui(self) -> None:
        """
        Update the screen UI.
        """
        y: int = -8
        self.health_bar.update(self.game)
        self.hotbar.update(self.game)
        self.score_label.update(self.game)
        self.camera_label.update(self.game)
        self.position_label.update(self.game)
        self.health_bar.center_horizontally(0, self.game.width).set_y(self.health_bar.get_height())
        self.hotbar.set_y(self.game.height - self.hotbar.get_height() - 16).center_horizontally(0, self.game.width)
        self.score_label.set_x(4)
        self.score_label.set_y(y)
        y += self.score_label.get_font_size() + 4
        self.camera_label.set_x(4)
        self.camera_label.set_y(y)
        y += self.camera_label.get_font_size() + 4
        self.position_label.set_x(4)
        self.position_label.set_y(y)
        self.health_bar.refresh()
        self.score_label.refresh()
        self.position_label.refresh()

    def set_state(self, state: bool) -> None:
        """
        Set the screen's visibility/interactivity.
        """
        super().set_state(state)
        self.score_label.set_state(state)
        self.camera_label.set_state(state)
        self.position_label.set_state(state)
        self.health_bar.set_state(state)
        self.hotbar.set_state(state)
