
from pygame import mouse, draw
from pygame.math import clamp

from game.gui.label import Widget, Label
from game.utils.logger import logger


class Button(Widget):

    MIN_WIDTH = 25
    MAX_WIDTH = 500
    MIN_HEIGHT = 25
    MAX_HEIGHT = 50

    def __init__(self, text="", x=0, y=0, width=200, height=50):
        super().__init__(x, y)
        self._width = width
        self._height = height
        self._background_colour = (255, 255, 255)
        self.label = Label(text, 0, 0).set_font_sizes((8, 10, 12))
        logger.debug(f'Created {__class__.__name__} with attributes {self.__dict__}')

    def draw(self, screen):
        background_colour = self._background_colour if not self.is_hovering_over() else \
            (self._background_colour[0] // 2,
             self._background_colour[1] // 2,
             self._background_colour[2] // 2)

        self.label.center_horizontally(self._x, self._width)
        self.label.center_vertically(self._y, self._height)

        draw.rect(screen, background_colour, (self._x, self._y, self._width, self._height), 2, 5)
        if self._width > self.label.get_total_width():
            self.label.draw(screen)

    def update(self, window):
        button_width = clamp(window.width * 0.25, Button.MIN_WIDTH, Button.MAX_WIDTH)
        button_height = clamp(window.height * 0.1, Button.MIN_HEIGHT, Button.MAX_HEIGHT)
        self.label.set_auto_font_size(window.width, window.height, window.max_width, window.max_height)
        self._width = button_width
        self._height = button_height
        self.refresh()

    def refresh(self):
        self.label.refresh()

    def is_hovering_over(self):
        mouse_x, mouse_y = mouse.get_pos()
        return (self._x <= mouse_x <= self._x + self._width and
                self._y <= mouse_y <= self._y + self._height and self._enabled)

    def center_horizontally(self, parent_x, parent_width):
        self._x = parent_x + parent_width / 2 - self._width / 2
        self.refresh()
        return self

    def center_vertically(self, parent_y, parent_height):
        self._y = parent_y + parent_height / 2 - self._height / 2
        self.refresh()
        return self

    def center(self, parent_x, parent_y, parent_width, parent_height):
        self.center_horizontally(parent_x, parent_width).center_vertically(parent_y, parent_height)
        return self

    def center_with_offset(self, parent_x, parent_y, parent_width, parent_height, x, y):
        self.center(parent_x, parent_y, parent_width, parent_height).offset(x, y)
        return self

    def set_width(self, width):
        self._width = width
        return self

    def get_width(self):
        return self._width

    def set_height(self, height):
        self._height = height
        return self

    def get_height(self):
        return self._height

    def set_background_colour(self, background_colour):
        self._background_colour = background_colour
        return self

    def get_background_colour(self):
        return self._background_colour
