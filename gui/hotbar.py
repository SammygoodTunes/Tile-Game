
from .widget import Widget
from .label import Label
from .slot import Slot
from data.items import Items
from pygame import Surface, SRCALPHA


class Hotbar(Widget):

    def __init__(self, x=0, y=0, slot_count=4):
        super().__init__(x, y)
        self._surface = None
        self._spacing = 4
        self._width = 0
        self._height = 0
        self._slots = [Slot() for i in range(slot_count)]
        self._tooltip = Label("")
        self._selected_slot = 0
        self._atlas = None
        self.init_slots()

    def init_slots(self):
        self._slots[0].set_item(Items.SHOVEL)
        for i, slot in enumerate(self._slots):
            new_x_pos = slot.get_width() * i + self._spacing * i
            slot.set_x(new_x_pos)
            self._width = new_x_pos + slot.get_width()
            self._height = slot.get_height()
        self._surface = Surface((self._width, self._height), SRCALPHA, 32).convert_alpha()
        for slot in self._slots:
            slot.draw(self._surface)
        self._tooltip.set_text(self.get_selected_slot_item().value.get_tooltip_name())

    def draw(self, screen):
        screen.blit(self._surface, (self._x, self._y, self._width, self._height))
        self._tooltip.draw(screen)

    def update(self, window):
        self._tooltip.update(window)
        self._tooltip.center_horizontally(0, window.width)
        self._tooltip.set_y(self._y - self._tooltip.get_total_height() - 5)
        for slot in self._slots:
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

    def set_selected_slot(self, slot_index):
        self._selected_slot = selected_slot
        self._slots[self._selected_slot].select()
        return self

    def select_slot(self, slot_index):
        self._selected_slot = slot_index
        self._slots[self._selected_slot].select()
        return self

    def unselect_slot(self, slot_index):
        self._slots[slot_index].unselect()

    def get_selected_slot(self):
        return self._selected_slot

    def get_selected_slot_item(self):
        return self._slots[self._selected_slot].get_item()

    def get_slot(self, slot_index):
        return self._slots[slot_index]

    def get_slots(self):
        return self._slots

    def set_atlas(self, atlas):
        self._atlas = atlas
        return self

    def get_atlas(self):
        return self._atlas
