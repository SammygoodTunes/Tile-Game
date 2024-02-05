
from .widget import Widget
from .slot import Slot
from pygame import Surface, SRCALPHA


class Hotbar(Widget):

    def __init__(self, x, y, slot_count):
        super().__init__(x, y)
        self._surface = None
        self._spacing = 4
        self._width = 0
        self._height = 0
        self.slots = [Slot(0, 0) for i in range(slot_count)]
        self.init_slots()

    def init_slots(self):
        for i, slot in enumerate(self.slots):
            new_x_pos = slot.get_width() * i + self._spacing * i
            slot.set_x(new_x_pos)
            self._width = new_x_pos + slot.get_width()
            self._height = slot.get_height()
        self._surface = Surface((self._width, self._height), SRCALPHA, 32).convert_alpha()
        for slot in self.slots:
            slot.draw(self._surface)

    def draw(self, screen):
        screen.blit(self._surface, (self._x, self._y, self._width, self._height))

    def update(self, window):
        for slot in self.slots:
            slot.update(window)
        self.init_slots()
        return self

    def center_horizontally(self, parent_x, parent_width):
        self._x = parent_x + parent_width / 2 - self._width / 2
        return self

    def center_vertically(self, parent_y, parent_height):
        self._y = parent_y + parent_height / 2 - self._height / 2
        return self

    def center(self, parent_x, parent_y, parent_width, parent_height):
        self.center_horizontally(parent_x, parent_width).center_vertically(parent_y, parent_height)
        return self

    def center_with_offset(self, parent_x, parent_y, parent_width, parent_height, x, y):
        self.center(parent_x, parent_y, parent_width, parent_height).offset(x, y)
        return self

    def set_spacing(self, spacing):
        self._spacing = spacing
        return self

    def get_spacing(self):
        return self._spacing

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
