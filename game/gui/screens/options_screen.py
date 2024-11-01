"""
Module name: options_screen
"""

from __future__ import annotations
from pygame import MOUSEBUTTONUP, MOUSEBUTTONDOWN
from pygame.event import Event
from typing import TYPE_CHECKING

if TYPE_CHECKING: from game.core.game import Game
from game.data.states.mouse_states import MouseStates
from game.gui.button import Button
from game.gui.checkbox import Checkbox
from game.gui.horizontal_slider import HorizontalSlider
from game.gui.label import Label
from game.gui.screens.screen import Screen
from game.gui.selectbox import SelectBox
from game.utils.translator import locales, translator as t, translator, get_locale_from_language


class OptionsScreen(Screen):
    """
    Class for creating the options screen.
    """

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self.faded_surface = None
        self.options_label = Label('OPTIONS')
        self.fps_limit_slider = (HorizontalSlider('FPS Limit')
                                 .set_value(game.fps_cap)
                                 .set_value_text(f'{game.fps_cap} FPS')
                                 .set_value_bounds(10, 1000))
        self.show_fps_box = Checkbox('Show FPS', checked=True)
        self.debug_info_box = Checkbox('Show debug info')
        self.vsync_box = Checkbox('Vsync', checked=True)
        self.language_list = SelectBox(tooltip_text='Language', width=200).set_values([value for value in locales.values()])
        self.back_button = Button('Back')

    def translate(self) -> None:
        self.options_label.set_text(t.t('screens.options.title'))
        self.fps_limit_slider.set_title(t.t('screens.options.fps_limit_slider'))
        self.show_fps_box.title_label.set_text(t.t('screens.options.show_fps_box'))
        self.debug_info_box.title_label.set_text(t.t('screens.options.debug_info_box'))
        self.language_list.set_tooltip_text(t.t('screens.options.language_list_tooltip'))

    def events(self, e: Event) -> None:
        if not self._enabled: return
        self.fps_limit_slider.events(e)
        self.show_fps_box.events(e)
        self.debug_info_box.events(e)
        self.vsync_box.events(e)

        if self.language_list.has_selected_a_value():
            translator.set('locale', get_locale_from_language(self.language_list.get_selected()))
            self.game.screens.perform_translation()

        self.language_list.events(e)
        if e.type == MOUSEBUTTONDOWN:
            if e.button == MouseStates.LMB:
                self.back_button.set_interact(not self.language_list.is_open())
        elif not e.type == MOUSEBUTTONUP:
            self.back_button.set_interact(not self.language_list.is_open())



        if self.game.fps_cap != self.fps_limit_slider.get_value():
            self.game.fps_cap = self.fps_limit_slider.get_value()
        self.language_list.update(self.game)
        self.fps_limit_slider.set_value_text(f'{self.game.fps_cap} FPS')

    def draw(self) -> None:
        if not self._enabled: return
        self.game.screen.blit(self.faded_surface, (0, 0))
        self.options_label.draw(self.game.screen)
        self.fps_limit_slider.draw(self.game.screen)
        self.show_fps_box.draw(self.game.screen)
        self.debug_info_box.draw(self.game.screen)
        self.vsync_box.draw(self.game.screen)
        self.language_list.draw(self.game)
        self.back_button.draw(self.game.screen)
        self.language_list.draw_value_list(self.game)

    def update_ui(self) -> None:
        if not self._enabled: return
        self.faded_surface = self.initialise_surface()
        self.fps_limit_slider.resize(self.game)
        self.show_fps_box.resize(self.game)
        self.debug_info_box.resize(self.game)
        self.vsync_box.resize(self.game)
        self.language_list.resize(self.game)
        self.back_button.resize(self.game)

        self.options_label.update(self.game)

        y = - 75 - self.options_label.get_height()
        self.options_label.center_with_offset(0, 0, self.game.width, self.game.height, 0, y)
        y += 75
        self.fps_limit_slider.center_with_offset(0, 0, self.game.width, self.game.height, 0, y)
        y += 30
        self.show_fps_box.center_with_offset(0, 0, self.game.width, self.game.height, -self.fps_limit_slider.get_width() // 2, y)
        y += 25
        self.debug_info_box.center_with_offset(0, 0, self.game.width, self.game.height, -self.fps_limit_slider.get_width() // 2, y)
        y += 25
        self.vsync_box.center_with_offset(0, 0, self.game.width, self.game.height, -self.fps_limit_slider.get_width() // 2, y)
        y += self.language_list.get_height()
        self.language_list.center_with_offset(0, 0, self.game.width, self.game.height, 0, y)
        y += 10 + self.back_button.get_height()
        self.back_button.center_with_offset(0, 0, self.game.width, self.game.height, 0, y)
        self.fps_limit_slider.update(self.game)
        self.show_fps_box.update(self.game)
        self.debug_info_box.update(self.game)
        self.vsync_box.update(self.game)
        self.language_list.update(self.game)
        self.back_button.update(self.game)

    def set_state(self, state: bool) -> None:
        super().set_state(state)
        self.options_label.set_state(state)
        self.fps_limit_slider.set_state(state)
        self.show_fps_box.set_state(state)
        self.debug_info_box.set_state(state)
        self.vsync_box.set_state(state)
        self.language_list.set_state(state)
        self.back_button.set_state(state)
        if state: self.update_ui()
        else: self.language_list.set_open(state)
