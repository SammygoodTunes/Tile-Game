
import pygame
from gui.screens.loading_screen import LoadingScreen
from gui.screens.pause_screen import PauseScreen
from gui.screens.options_screen import OptionsScreen
from data.mouse_properties import Mouse


class Screens:

    def __init__(self, window):
        self.window = window
        self.game = None
        self.screen = self.window.screen
        self.loading_screen = LoadingScreen(window)
        self.pause_screen = PauseScreen(window)
        self.options_screen = OptionsScreen(window)

    def link_game(self, game_obj):
        self.game = game_obj
        self.options_screen.game = self.game

    def events(self, e):
        self.loading_screen.events(e)
        self.options_screen.events(e)
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                if self.options_screen.get_state():
                    self.options_screen.set_state(not self.options_screen.get_state())
                else:
                    self.pause_screen.set_state(not self.pause_screen.get_state())
                self.window.paused = self.pause_screen.get_state()
        if e.type == pygame.MOUSEBUTTONUP:
            if e.button == Mouse.LMB:
                if self.pause_screen.resume_button.is_hovering_over():
                    self.pause_screen.set_state(False)
                    self.window.paused = False
                elif self.pause_screen.options_button.is_hovering_over():
                    self.pause_screen.set_state(False)
                    self.options_screen.set_state(True)
                elif self.pause_screen.quit_button.is_hovering_over():
                    self.window.stop()
                elif self.options_screen.back_button.is_hovering_over():
                    self.options_screen.set_state(False)
                    self.pause_screen.set_state(True)

    def update(self):
        self.loading_screen.draw(self.screen)
        self.pause_screen.draw(self.screen)
        self.options_screen.draw(self.screen)

    def update_ui(self):
        self.loading_screen.update_ui()
        self.pause_screen.update_ui()
        self.options_screen.update_ui()

