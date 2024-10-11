
from pygame import MOUSEBUTTONUP, Surface
from pygame.event import Event

from game.data.properties.screen_properties import ScreenProperties
from game.gui.screens.screen import Screen
from game.gui.label import Label
from game.gui.button import Button
from game.data.states.mouse_states import MouseStates


class CreditsScreen(Screen):
    """
    Class for creating the credits screen.
    """

    def __init__(self, window) -> None:
        super().__init__()
        self.window = window
        self.faded_surface = self.initialise_surface()
        self.options_label = Label('Credits')
        self.prog_title_label = Label('Programming by:')
        self.art_title_label = Label('Art by:')
        self.font_title_label = Label('Font by:')
        self.prog_value_label = Label('SammygoodTunes').set_colour((255, 255, 0))
        self.art_value_label = Label('Pickmonde\nJatzylap\nSammygoodTunes').set_colour((255, 255, 0))
        self.font_value_label = Label('OmegaPC777').set_colour((255, 255, 0))
        self.back_button = Button("Back")

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
        Track the screen events.
        """
        if e.type == MOUSEBUTTONUP:
            if e.button == MouseStates.LMB:
                if self.back_button.is_hovering_over():
                    self._enabled = False

    def draw(self) -> None:
        """
        Draw the screen and its components.
        """
        if not self._enabled:
            return
        self.window.screen.blit(self.faded_surface, (0, 0))
        self.options_label.draw(self.window.screen)
        self.prog_title_label.draw(self.window.screen)
        self.prog_value_label.draw(self.window.screen)
        self.art_title_label.draw(self.window.screen)
        self.art_value_label.draw(self.window.screen)
        self.font_title_label.draw(self.window.screen)
        self.font_value_label.draw(self.window.screen)
        self.back_button.draw(self.window.screen)

    def update_ui(self) -> None:
        """
        Update the screen GUI.
        """
        if not self._enabled:
            return
        y = -50 - 40 - self.options_label.font.size(self.options_label.get_text())[1]
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
        y += self.font_title_label.get_total_height() * 3
        self.font_title_label.update(self.window)
        self.font_title_label.center_with_offset(0, 0, self.window.width, self.window.height, -self.font_title_label.get_total_width() // 2 - 10, y)
        self.font_value_label.update(self.window)
        self.font_value_label.center_with_offset(0, 0, self.window.width, self.window.height, self.font_value_label.get_total_width() // 2 + 10, y)
        y += 20 + self.font_value_label.get_total_height()
        self.back_button.update(self.window)
        self.back_button.center_with_offset(0, 0, self.window.width, self.window.height, 0, y)

    def set_state(self, state: bool) -> None:
        """
        Set the screen's visibility/interactivity.
        """
        super().set_state(state)
        self.options_label.set_state(state)
        self.prog_title_label.set_state(state)
        self.prog_value_label.set_state(state)
        self.art_title_label.set_state(state)
        self.art_value_label.set_state(state)
        self.font_title_label.set_state(state)
        self.font_value_label.set_state(state)
        self.back_button.set_state(state)
        if state: self.update_ui()
