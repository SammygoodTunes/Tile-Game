
import pygame
from gui.screens.mainmenu_screen import MainMenu
from gui.screens.loading_screen import LoadingScreen
from gui.screens.pause_screen import PauseScreen
from gui.screens.options_screen import OptionsScreen
from data.mouse_properties import Mouse


class Screens:

    def __init__(self, window):
        self.window = window
        self.game = None
        self.screen = self.window.screen
        self.main_menu = MainMenu(window)
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
            if e.key == pygame.K_ESCAPE and self.game.start_game:
                if self.options_screen.get_state():
                    self.options_screen.set_state(not self.options_screen.get_state())
                else:
                    self.pause_screen.set_state(not self.pause_screen.get_state())
                self.window.paused = self.pause_screen.get_state()
        if e.type == pygame.MOUSEBUTTONUP:
            if e.button == Mouse.LMB:

                if self.options_screen.back_button.is_hovering_over():
                    self.options_screen.set_state(False)
                    if self.game.start_game:
                        self.pause_screen.set_state(True)
                    else:
                        self.main_menu.set_state(True)

                elif self.main_menu.play_button.is_hovering_over() and self.main_menu.get_state():
                    self.window.start_game = True
                    self.main_menu.set_state(False)
                    self.game.world.initialise()
                elif self.main_menu.quit_button.is_hovering_over() and self.main_menu.get_state():
                    self.window.stop()
                elif self.main_menu.options_button.is_hovering_over() and self.main_menu.get_state():
                    self.options_screen.set_state(True)
                    self.main_menu.set_state(False)

                elif self.pause_screen.resume_button.is_hovering_over():
                    self.pause_screen.set_state(False)
                    self.window.paused = False
                elif self.pause_screen.options_button.is_hovering_over():
                    self.pause_screen.set_state(False)
                    self.options_screen.set_state(True)
                elif self.pause_screen.quit_button.is_hovering_over():
                    self.window.start_game = False
                    self.pause_screen.set_state(False)
                    self.main_menu.set_state(True)

    def update(self):
        self.main_menu.draw()
        self.loading_screen.draw()
        self.pause_screen.draw()
        self.options_screen.draw()

    def update_ui(self):
        self.main_menu.update_ui()
        self.loading_screen.update_ui()
        self.pause_screen.update_ui()
        self.options_screen.update_ui()

