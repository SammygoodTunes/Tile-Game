"""
Module name: options_screen
"""

from pygame import MOUSEBUTTONUP, Surface
from pygame.event import Event

from game.data.properties.screen_properties import ScreenProperties
from game.gui.screens.screen import Screen
from game.gui.label import Label
from game.gui.button import Button
from game.gui.horizontal_slider import HorizontalSlider
from game.gui.checkbox import Checkbox
from game.data.states.mouse_states import MouseStates


class OptionsScreen(Screen):
    """
    Class for creating the options screen.
    """

    def __init__(self, window) -> None:
        super().__init__()
        self.window = window
        self.faded_surface = self.initialise_surface()
        self.options_label = Label('OPTIONS')
        self.fps_limit_slider = (HorizontalSlider('FPS Limit')
                                 .set_value(window.fps_cap)
                                 .set_value_text(f'{window.fps_cap} FPS')
                                 .set_value_bounds(10, 1000))
        self.show_fps_box = Checkbox('Show FPS', checked=True)
        self.debug_info_box = Checkbox('Show debug info')
        self.vsync_box = Checkbox('Vsync', checked=True)
        self.back_button = Button('Back')

    def initialise_surface(self) -> Surface:
        """
        Initialise the screen's surface.
        """
        surface = Surface((self.window.width, self.window.height))
        surface.fill((0, 0, 0))
        surface.set_alpha(ScreenProperties.ALPHA)
        return surface

    def events(self, e: Event) -> None:
        """
        Handle the screen events.
        """
        self.fps_limit_slider.events(e)
        self.show_fps_box.events(e)
        self.debug_info_box.events(e)
        self.vsync_box.events(e)
        if e.type == MOUSEBUTTONUP:
            if e.button == MouseStates.LMB:
                if self.back_button.is_hovering_over():
                    self._enabled = False
        if self.window.fps_cap != self.fps_limit_slider.get_value():
            self.window.fps_cap = self.fps_limit_slider.get_value()
        self.fps_limit_slider.set_value_text(f'{self.window.fps_cap} FPS')

    def draw(self) -> None:
        """
        Draw the screen and its components.
        """
        if not self._enabled:
            return
        self.window.screen.blit(self.faded_surface, (0, 0))
        self.options_label.draw(self.window.screen)
        self.fps_limit_slider.draw(self.window.screen)
        self.show_fps_box.draw(self.window.screen)
        self.debug_info_box.draw(self.window.screen)
        self.vsync_box.draw(self.window.screen)
        self.back_button.draw(self.window.screen)

    def update_ui(self) -> None:
        """
        Update the screen UI.
        """
        if not self._enabled:
            return
        self.faded_surface = self.initialise_surface()
        y = - 75 - self.options_label.font.size(self.options_label.get_text())[1]
        self.options_label.update(self.window)
        self.options_label.center_with_offset(0, 0, self.window.width, self.window.height, 0, y)
        y += 75
        self.fps_limit_slider.update(self.window)
        self.fps_limit_slider.center_with_offset(0, 0, self.window.width, self.window.height, 0, y)
        y += 30
        self.show_fps_box.update(self.window)
        self.show_fps_box.center_with_offset(0, 0, self.window.width, self.window.height, -self.fps_limit_slider.get_width() // 2, y)
        y += 25
        self.debug_info_box.update(self.window)
        self.debug_info_box.center_with_offset(0, 0, self.window.width, self.window.height, -self.fps_limit_slider.get_width() // 2, y)
        y += 25
        self.vsync_box.update(self.window)
        self.vsync_box.center_with_offset(0, 0, self.window.width, self.window.height, -self.fps_limit_slider.get_width() // 2, y)
        y += 5 + self.back_button.get_height()
        self.back_button.update(self.window)
        self.back_button.center_with_offset(0, 0, self.window.width, self.window.height, 0, y)

    def set_state(self, state: bool) -> None:
        """
        Set the screen's visibility/interactivity.
        """
        super().set_state(state)
        self.options_label.set_state(state)
        self.fps_limit_slider.set_state(state)
        self.show_fps_box.set_state(state)
        self.debug_info_box.set_state(state)
        self.vsync_box.set_state(state)
        self.back_button.set_state(state)
        if state: self.update_ui()
