
from game.gui.widget import Widget
from game.gui.label import Label
from game.data.mouse_properties import Mouse
import pygame


class Checkbox(Widget):

    def __init__(self, title, x=0, y=0, checked=False):
        super().__init__(x, y)
        self._checked = checked
        self._colour = (255, 255, 255)
        self._size = 20
        self._spacing = 8
        self.title_label = Label(title, self._x + self._size + self._spacing, self._y).set_font_sizes((7, 8, 10))

    def draw(self, screen):
        if self._checked:
            pygame.draw.rect(screen, self._colour, (self._x + 4, self._y + 4, self._size - 8, self._size - 8), border_radius=0)
        pygame.draw.rect(screen, self._colour, (self._x, self._y, self._size, self._size), width=2, border_radius=2)
        self.title_label.draw(screen)

    def events(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == Mouse.LMB and self.is_hovering_over():
                self._checked = not self._checked

    def update(self, window):
        self.title_label.set_auto_font_size(window.width, window.height, window.max_width, window.max_height)
        self.refresh()

    def refresh(self):
        width, height = self.title_label.font.size(self.title_label.get_text())
        self.title_label.center_horizontally(width / 2 + self._x + self._size + self._spacing, self._size)
        self.title_label.center_vertically(self._y, self._size)
        self.title_label.refresh()

    def is_hovering_over(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        width = self.title_label.font.size(self.title_label.get_text())[0]
        return (self._x <= mouse_x <= self._x + self._size + self._spacing * 2 + width and
                self._y <= mouse_y <= self._y + self._size and self._enabled)

    def center_horizontally(self, parent_x, parent_width):
        self._x = parent_x + parent_width / 2 - self._size / 2
        self.refresh()
        return self

    def center_vertically(self, parent_y, parent_height):
        self._y = parent_y + parent_height / 2 - self._size / 2
        self.refresh()
        return self

    def center(self, parent_x, parent_y, parent_width, parent_height):
        self.center_horizontally(parent_x, parent_width).center_vertically(parent_y, parent_height)
        return self

    def center_with_offset(self, parent_x, parent_y, parent_width, parent_height, x, y):
        self.center(parent_x, parent_y, parent_width, parent_height).offset(x, y)
        self.refresh()
        return self

    def set_size(self, size):
        self._size = size
        return self

    def get_size(self):
        return self._size

    def set_checked(self, state):
        self._checked = state
        return self

    def is_checked(self):
        return self._checked

    def offset_x(self, offset_x):
        super().offset_x(offset_x)
        self.title_label.set_x(self.title_label.get_x() + offset_x)
        self.title_label.set_shadow_x_offset(2)
        return self

    def offset_y(self, offset_y):
        super().offset_y(offset_y)
        self.title_label.set_y(self.title_label.get_y() + offset_y)
        self.title_label.set_shadow_y_offset(2)
        return self
