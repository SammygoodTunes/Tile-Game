import pygame
from game.gui.screens.screen import Screen
from game.gui.label import Label
from game.gui.button import Button
from game.data.mouse_properties import Mouse


class CreditsScreen(Screen):

    def __init__(self, window):
        super().__init__()
        self.window = window
        self.faded_surface = self.initialise_surface()
        self.options_label = Label("Credits")
        self.prog_title_label = Label("Programming by:")
        self.art_title_label = Label("Art by:")
        self.prog_value_label = Label("SammygoodTunes").set_colour((255, 255, 0))
        self.art_value_label = Label("Pickmonde, SammygoodTunes").set_colour((255, 255, 0))
        self.back_button = Button("Back")

    def initialise_surface(self):
        surface = pygame.Surface((self.window.width, self.window.height))
        surface.fill((0, 0, 0))
        surface.set_alpha(96)
        return surface

    def events(self, e):
        if e.type == pygame.MOUSEBUTTONUP:
            if e.button == Mouse.LMB:
                if self.back_button.is_hovering_over():
                    self._enabled = False

    def draw(self):
        if self._enabled:
            self.window.screen.blit(self.faded_surface, (0, 0))
            self.options_label.draw(self.window.screen)
            self.prog_title_label.draw(self.window.screen)
            self.prog_value_label.draw(self.window.screen)
            self.art_title_label.draw(self.window.screen)
            self.art_value_label.draw(self.window.screen)
            self.back_button.draw(self.window.screen)

    def update_ui(self):
        y = -50 - 25 - self.options_label.font.size(self.options_label.get_text())[1]
        self.faded_surface = self.initialise_surface()
        self.options_label.update(self.window)
        self.options_label.center_with_offset(0, 0, self.window.width, self.window.height, 0, y)
        y += 10 + self.prog_title_label.get_total_height()
        self.prog_title_label.update(self.window)
        self.prog_title_label.center_with_offset(0, 0, self.window.width, self.window.height, -self.prog_title_label.get_total_width() // 2 - 10, y)
        self.prog_value_label.update(self.window)
        self.prog_value_label.center_with_offset(0, 0, self.window.width, self.window.height, self.prog_value_label.get_total_width() // 2 + 10, y)
        y += 5 + self.art_title_label.get_total_height()
        self.art_title_label.update(self.window)
        self.art_title_label.center_with_offset(0, 0, self.window.width, self.window.height, -self.art_title_label.get_total_width() // 2 - 10, y)
        self.art_value_label.update(self.window)
        self.art_value_label.center_with_offset(0, 0, self.window.width, self.window.height, self.art_value_label.get_total_width() // 2 + 10, y)
        self.back_button.update(self.window)
        self.back_button.center_with_offset(0, 0, self.window.width, self.window.height, 0, self.back_button.get_height() + 5)

    def set_state(self, state):
        super().set_state(state)
        self.options_label.set_state(state)
        self.prog_title_label.set_state(state)
        self.prog_value_label.set_state(state)
        self.art_title_label.set_state(state)
        self.art_value_label.set_state(state)
        self.back_button.set_state(state)
