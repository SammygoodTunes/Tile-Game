"""
Module name: tooltip
"""

from pygame import mouse, Surface
from pygame.draw import rect

from game.data.properties.screen_properties import ScreenProperties
from game.gui.label import Label
from game.gui.widget import Widget


class Tooltip(Widget):
    """
    Class for creating a tooltip.
    """

    def __init__(self, x: int = 0, y: int = 0, text: str = '') -> None:
        super().__init__(x, y)
        self._label = Label(text=text).set_font_sizes((8, 9, 10))
        self._surface = self.initialise_surface()

    def initialise_surface(self) -> Surface:
        """
        Initialise the tooltip's surface.
        """
        surface = Surface((self._label.get_total_width() + 10, self._label.get_total_height() + 5))
        surface.fill((0, 0, 0))
        surface.set_alpha(ScreenProperties.PRONOUNCED_ALPHA)
        return surface

    def draw(self, screen) -> None:
        """
        Draw the tooltip and its components.
        """
        if not self._enabled or not self._label.get_text():
            return
        x, y = mouse.get_pos()[0] - self._surface.get_width(), mouse.get_pos()[1] - self._surface.get_height()
        screen.blit(self._surface, (x, y))
        rect(screen, (255, 255, 255), (x, y, self._surface.get_width(), self._surface.get_height()), width=2)
        self._label.center(x, y, self._surface.get_width(), self._surface.get_height()).draw(screen)

    def update(self, window) -> None:
        """
        Update the tooltip and its components.
        """
        self._label.update(window)
        self._surface = self.initialise_surface()
