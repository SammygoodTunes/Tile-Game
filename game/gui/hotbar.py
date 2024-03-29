
from pygame import Surface, SRCALPHA

from game.data.items import Items
from game.gui.label import Label
from game.gui.slot import Slot
from game.gui.widget import Widget
from game.utils.logger import logger


class Hotbar(Widget):
    """
    Class for creating a hotbar.
    """

    def __init__(self, x=0, y=0, slot_count=4):
        super().__init__(x, y)
        self._surface = None
        self._spacing = 4
        self._width = 0
        self._height = 0
        self._slots = [Slot() for _ in range(slot_count)]
        self._tooltip = Label("")
        self._selected_slot = 0
        self._atlas = None
        self.init_slots()
        logger.debug(f'Created {__class__.__name__} with attributes {self.__dict__}')

    def init_slots(self):
        """
        Initialise the hotbar's slots.
        """
        self._slots[0].set_item(Items.SHOVEL)
        for i, slot in enumerate(self._slots):
            new_x_pos = slot.get_width() * i + self._spacing * i
            slot.set_x(new_x_pos)
            self._width = new_x_pos + slot.get_width()
            self._height = slot.get_height()
        self._surface = Surface((self._width, self._height), SRCALPHA, 32).convert_alpha()
        for slot in self._slots:
            slot.draw(self._surface)
        self._tooltip.set_text(self.get_selected_slot_item().get_tooltip_name())

    def draw(self, screen):
        """
        Draw the hotbar and its components.
        """
        screen.blit(self._surface, (self._x, self._y, self._width, self._height))
        self._tooltip.draw(screen)

    def update(self, window):
        """
        Update the hotbar and its components.
        """
        self._tooltip.update(window)
        self._tooltip.center_horizontally(0, window.width)
        self._tooltip.set_y(self._y - self._tooltip.get_total_height() - 5)
        for slot in self._slots:
            slot.update(window)
        self.init_slots()
        return self

    def center_horizontally(self, parent_x, parent_width):
        """
        Center the hotbar horizontally relative to the specified parent, then return the hotbar itself.
        """
        self._x = parent_x + parent_width / 2 - self._width / 2
        return self

    def center_vertically(self, parent_y, parent_height):
        """
        Center the hotbar vertically relative to the specified parent, then return the hotbar itself.
        """
        self._y = parent_y + parent_height / 2 - self._height / 2
        return self

    def center(self, parent_x, parent_y, parent_width, parent_height):
        """
        Center the hotbar on both axes relative to the specified parent, then return the hotbar itself.
        """
        self.center_horizontally(parent_x, parent_width).center_vertically(parent_y, parent_height)
        return self

    def center_with_offset(self, parent_x, parent_y, parent_width, parent_height, x, y):
        """
        Center the hotbar with center() and offset it by x and y relative to the specified parent, then return
        the hotbar itself.
        """
        self.center(parent_x, parent_y, parent_width, parent_height).offset(x, y)
        return self

    def set_spacing(self, spacing):
        """
        Set the spacing between the hotbar's slots, then return the hotbar itself.
        """
        self._spacing = spacing
        return self

    def get_spacing(self):
        """
        Return the spacing between the hotbar's slots.
        """
        return self._spacing

    def set_width(self, width):
        """
        Set the width of the hotbar, then return the hotbar itself.
        """
        self._width = width
        return self

    def get_width(self):
        """
        Return the width of the hotbar.
        """
        return self._width

    def set_height(self, height):
        """
        Set the height of the hotbar, then return the hotbar itself.
        """
        self._height = height
        return self

    def get_height(self):
        """
        Return the height of the hotbar.
        """
        return self._height

    def select_slot(self, slot_index):
        """
        Select a hotbar slot, then return the hotbar itself.
        """
        self._selected_slot = slot_index
        self._slots[self._selected_slot].select()
        return self

    def unselect_slot(self, slot_index):
        """
        Unselect a hotbar slot, then return the slot itself.
        """
        self._slots[slot_index].unselect()
        return self

    def get_selected_slot(self):
        """
        Return the selected slot of the hotbar.
        """
        return self._selected_slot

    def get_selected_slot_item(self):
        """
        Return the item of the selected hotbar slot.
        """
        return self._slots[self._selected_slot].get_item()

    def get_slot(self, slot_index):
        """
        Return the slot object of the hotbar at specified index.
        """
        return self._slots[slot_index]

    def get_slots(self):
        """
        Return all hotbar slots.
        """
        return self._slots

    def set_atlas(self, atlas):
        """
        Set the texture atlas that will be used by the hotbar, then return the hotbar itself.
        """
        self._atlas = atlas
        return self

    def get_atlas(self):
        """
        Return the texture atlas used by the hotbar.
        """
        return self._atlas
