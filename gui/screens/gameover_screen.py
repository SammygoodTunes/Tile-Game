
import pygame
from .screen import Screen
from gui.label import Label
from gui.button import Button


class GameoverScreen(Screen):

    def __init__(self, window):
        super().__init__()
        self.window = window
        self.faded_surface = self.initialise_surface()
        self.gameover_label = Label(text="You died.")
        self.regen_button = Button(text="Regenerate")
        self.quit_button = Button(text="Quit")

    def initialise_surface(self):
        surface = pygame.Surface((self.window.width, self.window.height))
        surface.fill((0, 0, 0))
        surface.set_alpha(96)
        return surface

    def draw(self):
        if self._enabled:
            self.window.screen.blit(self.faded_surface, (0, 0))
            self.gameover_label.draw(self.window.screen)
            self.regen_button.draw(self.window.screen)
            self.quit_button.draw(self.window.screen)

    def update_ui(self):
        self.faded_surface = self.initialise_surface()
        self.gameover_label.update(self.window)
        self.gameover_label.center_with_offset(0, 0, self.window.width, self.window.height, 0, -self.regen_button.get_height() - 25 - self.gameover_label.get_total_height())
        self.regen_button.update(self.window)
        self.regen_button.center_with_offset(0, 0, self.window.width, self.window.height, 0, -self.quit_button.get_height() - 5)
        self.quit_button.update(self.window)
        self.quit_button.center_with_offset(0, 0, self.window.width, self.window.height, 0, 5)

    def set_state(self, state):
        super().set_state(state)
        self.gameover_label.set_state(state)
        self.regen_button.set_state(state)
        self.quit_button.set_state(state)
