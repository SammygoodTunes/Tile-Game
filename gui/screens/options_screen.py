import pygame
from .screen import Screen
from gui.label import Label
from gui.button import Button
from gui.horizontal_slider import HorizontalSlider
from gui.checkbox import Checkbox
from data.mouse_properties import Mouse
from random import randint


class OptionsScreen(Screen):

    def __init__(self, window):
        super().__init__()
        self.window = window
        self.game = None
        self.faded_surface = self.initialise_surface()
        self.options_label = Label("Options")
        self.fps_limit_slider = HorizontalSlider("FPS Limit").set_value(window.fps_cap).set_value_bounds(10, 1000)
        self.show_fps_box = Checkbox("Show FPS", checked=True)
        self.debug_info_box = Checkbox("Show debug info", checked=False)
        self.back_button = Button("Back")

    def initialise_surface(self):
        surface = pygame.Surface((self.window.width, self.window.height))
        surface.fill((0, 0, 0))
        surface.set_alpha(128)
        return surface

    def events(self, e):
        self.fps_limit_slider.events(e)
        self.show_fps_box.events(e)
        self.debug_info_box.events(e)
        if e.type == pygame.MOUSEBUTTONUP:
            if e.button == Mouse.LMB:
                if self.back_button.is_hovering_over():
                    self._enabled = False
        if self.window.fps_cap != self.fps_limit_slider.get_value():
            self.window.fps_cap = self.fps_limit_slider.get_value()

    def draw(self):
        if self._enabled:
            self.window.screen.blit(self.faded_surface, (0, 0))
            self.options_label.draw(self.window.screen)
            self.fps_limit_slider.draw(self.window.screen)
            self.show_fps_box.draw(self.window.screen)
            self.debug_info_box.draw(self.window.screen)
            self.back_button.draw(self.window.screen)

    def update_ui(self):
        self.faded_surface = self.initialise_surface()
        self.options_label.update(self.window)
        self.options_label.center_with_offset(0, 0, self.window.width, self.window.height, 0, -50 - 25 - self.options_label.font.size(self.options_label.get_text())[1])
        self.fps_limit_slider.update(self.window)
        self.fps_limit_slider.center_with_offset(0, 0, self.window.width, self.window.height, 0, -self.options_label.font.size(self.options_label.get_text())[1] - 25)
        self.show_fps_box.update(self.window)
        self.show_fps_box.center_with_offset(0, 0, self.window.width, self.window.height, -self.fps_limit_slider.get_width() // 2, -25)
        self.debug_info_box.update(self.window)
        self.debug_info_box.center_with_offset(0, 0, self.window.width, self.window.height, -self.fps_limit_slider.get_width() // 2, 0)
        self.back_button.update(self.window)
        self.back_button.center_with_offset(0, 0, self.window.width, self.window.height, 0, self.back_button.get_height() + 5)

    def set_state(self, state):
        super().set_state(state)
        self.options_label.set_state(state)
        self.fps_limit_slider.set_state(state)
        self.show_fps_box.set_state(state)
        self.debug_info_box.set_state(state)
        self.back_button.set_state(state)
