"""
Module name: servercreate_screen
"""


from __future__ import annotations

from socket import create_server

from pygame import MOUSEBUTTONDOWN, MOUSEBUTTONUP
from pygame.event import Event
from typing import TYPE_CHECKING

from game.gui.screens.fx_screen import FxScreen

if TYPE_CHECKING: from game.core.game import Game
from game.data.properties.player_properties import PlayerProperties
from game.data.properties.world_properties import WorldProperties
from game.data.states.mouse_states import MouseStates
from game.gui.button import Button
from game.gui.inputbox import InputBox
from game.gui.label import Label
from game.gui.ordering_container import OrderingContainer
from game.gui.screens.screen import Screen
from game.gui.selectbox import SelectBox
from game.world.theme_manager import ThemeManager
from game.utils.translator import translator as t


class ServerCreateScreen(Screen):
    """
    Class for creating the server create screen.
    """

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self.faded_surface = None
        self.create_label = Label("Create server")
        self.ign_input = (InputBox(placeholder_text='Player name', tooltip_text='Player name').
                          set_max_text_length(PlayerProperties.MAX_PLAYER_NAME_SIZE).authorise_only_alnumlines())
        self.seed_input = InputBox(placeholder_text='Seed', tooltip_text='Seed').authorise_only_alnum()
        self.world_theme_select = SelectBox(tooltip_text='World Theme')
        self.world_size_select = SelectBox(tooltip_text='World Size').set_values([
            WorldProperties.MAP_SMALL,
            WorldProperties.MAP_MEDIUM,
            WorldProperties.MAP_LARGE,
        ])
        self.ordering_container = OrderingContainer().set_widgets([
            self.ign_input,
            self.seed_input
        ])
        self.create_button = Button('Create')
        self.back_button = Button('Back')
        self.initialise_themes()

    def initialise_themes(self) -> None:
        """
        Initialise the world theme select box.
        """
        self.world_theme_select.set_values(ThemeManager.get_theme_names())

    def events(self, e: Event) -> None:
        if not self._enabled: return
        for widget in self.ordering_container.get_widgets():
            widget.events(e)
        self.world_theme_select.events(e)
        self.world_size_select.events(e)
        self.create_button.set_state(bool(self.ign_input.get_text().strip()))
        state = (not self.world_theme_select.is_open() and
                 not self.world_size_select.is_open())
        if e.type == MOUSEBUTTONDOWN:
            if e.button == MouseStates.LMB:
                self.create_button.set_interact(state)
                self.back_button.set_interact(state)
                self.ordering_container.set_interact(state)
                self.world_theme_select.set_interact(not self.world_size_select.is_open())
                self.world_size_select.set_interact(not self.world_theme_select.is_open())
        elif not e.type == MOUSEBUTTONUP:
            self.create_button.set_interact(state)
            self.back_button.set_interact(state)
            self.ordering_container.set_interact(state)
            self.world_theme_select.set_interact(not self.world_size_select.is_open())
            self.world_size_select.set_interact(not self.world_theme_select.is_open())
        self.ordering_container.events(e)

    def translate(self) -> None:
        self.initialise_themes()
        self.ign_input.set_placeholder_text(t.t('screens.servercreate.ign_input_placeholder'))
        self.ign_input.set_tooltip_text(t.t('screens.servercreate.ign_input_placeholder'))
        self.seed_input.set_placeholder_text(t.t('screens.servercreate.seed_input_placeholder'))
        self.seed_input.set_tooltip_text(t.t('screens.servercreate.seed_input_placeholder'))
        self.world_theme_select.set_tooltip_text(t.t('screens.servercreate.world_theme_select_tooltip'))
        self.world_size_select.set_tooltip_text(t.t('screens.servercreate.world_size_select_tooltip'))
        self.create_label.set_text(t.t('screens.servercreate.create_label'))
        self.back_button.label.set_text(t.t('screens.general.back_button'))

    def draw(self) -> None:
        if not self._enabled: return
        FxScreen.draw_falling_snow_layer(screen=self.game.screen)
        self.game.screen.blit(self.faded_surface, (0, 0))
        self.create_label.draw(self.game.screen)
        for widget in self.ordering_container.get_widgets():
            if isinstance(widget, InputBox):
                widget.draw(self.game.screen)
        self.create_button.draw(self.game.screen)
        self.back_button.draw(self.game.screen)
        self.world_theme_select.draw(self.game)
        self.world_size_select.draw(self.game)
        self.world_size_select.draw_value_list(self.game)
        self.world_theme_select.draw_value_list(self.game)

    def update_ui(self) -> None:
        if not self._enabled: return
        self.faded_surface = self.initialise_surface()
        self.create_button.resize(self.game)
        self.world_theme_select.resize(self.game)
        self.world_size_select.resize(self.game)
        self.back_button.resize(self.game)
        self.create_label.update(self.game)
        self.create_label.center_with_offset(
            0,
            0,
            self.game.width,
            self.game.height,
            0,
            -self.seed_input.get_height()
            - self.create_label.get_height()
            - self.world_theme_select.get_height()
            - 25
        )
        self.ign_input.center_with_offset(
            0,
            0,
            self.game.width,
            self.game.height,
            0,
            -self.seed_input.get_height() - self.world_theme_select.get_height() - 10
        )
        self.seed_input.center_with_offset(
            0,
            0,
            self.game.width,
            self.game.height,
            0,
            -self.world_theme_select.get_height() - 5
        )
        self.world_theme_select.center(0, 0, self.game.width, self.game.height)
        self.world_size_select.center_with_offset(
            0,
            0,
            self.game.width,
            self.game.height,
            0,
            self.world_theme_select.get_height() + 5
        )
        self.create_button.center_with_offset(
            0,
            0,
            self.game.width,
            self.game.height,
            0,
            self.world_theme_select.get_height()
            + self.world_size_select.get_height()
            + 15
        )
        self.back_button.center_with_offset(
            0,
            0,
            self.game.width,
            self.game.height,
            0,
            self.world_theme_select.get_height()
            + self.world_size_select.get_height()
            + self.create_button.get_height()
            + 20
        )
        self.ign_input.update(self.game)
        self.seed_input.update(self.game)
        self.world_theme_select.update(self.game)
        self.world_size_select.update(self.game)
        self.create_button.update(self.game)
        self.back_button.update(self.game)
        self.create_button.set_state(bool(self.ign_input.get_text().strip()))

    def set_state(self, state: bool) -> None:
        super().set_state(state)
        self.create_label.set_state(state)
        self.ign_input.set_state(state)
        self.seed_input.set_state(state)
        self.world_theme_select.set_state(state)
        self.world_size_select.set_state(state)
        self.create_button.set_state(state)
        self.back_button.set_state(state)
        self.ordering_container.set_state(state)
        if state: self.update_ui()
        else:
            self.ign_input.set_selected(state)
            self.seed_input.set_selected(state)
            self.world_theme_select.set_open(state)
            self.world_size_select.set_open(state)
