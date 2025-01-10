"""
Module name: hotbar
"""

from __future__ import annotations
from pygame import Surface, SRCALPHA
from typing import Self

from game.core.window import Window
from game.data.items.items import Items
from game.data.items.item import Item
from game.gui.label import Label
from game.gui.slot import Slot
from game.gui.widget import Widget


class Hotbar(Widget):
    """
    Class for creating a hotbar.
    """

    def __init__(self, x: int = 0, y: int = 0, slot_count: int = 4) -> None:
        super().__init__(x, y)
        self._surface: Surface | None = None
        self._spacing = 4
        self._slots = [Slot() for _ in range(slot_count)]
        self._tooltip = Label()
        self._selected_slot = 0
        self._atlas: Surface | None = None

    def init_slots(self) -> None:
        """
        Initialise the hotbar's slots.
        """
        self._surface = Surface((self._width, self._height), SRCALPHA, 32).convert_alpha()
        self._slots[0].set_item(Items.SHOVEL)
        self._slots[1].set_item(Items.GUN)
        for i, slot in enumerate(self._slots):
            new_x_pos = slot.get_width() * i + self._spacing * i
            slot.set_x(new_x_pos)
            self._width = new_x_pos + slot.get_width()
            self._height = slot.get_height()
        for slot in self._slots:
            slot.draw(self._surface)
        self._tooltip.set_text(self.get_selected_slot_item().get_tooltip_name())

    def draw(self, screen) -> None:
        screen.blit(self._surface, (self._x, self._y, self._width, self._height))
        self._tooltip.draw(screen)

    def update(self, window: Window) -> None:
        self._tooltip.center_horizontally(0, window.width)
        self._tooltip.set_y(self._y - self._tooltip.get_height() - 5)
        self._tooltip.update(window)
        for slot in self._slots:
            slot.update(window)
        self.init_slots()

    def set_spacing(self, spacing: int) -> Self:
        """
        Set the spacing between the hotbar's slots, then return the hotbar itself.
        """
        self._spacing = spacing
        return self

    def get_spacing(self) -> int:
        """
        Return the spacing between the hotbar's slots.
        """
        return self._spacing

    def select_slot(self, slot_index: int) -> Self:
        """
        Select a hotbar slot, then return the hotbar itself.
        """
        self._selected_slot = slot_index
        self._slots[self._selected_slot].select()
        return self

    def unselect_slot(self, slot_index: int) -> Self:
        """
        Unselect a hotbar slot, then return the slot itself.
        """
        self._slots[slot_index].unselect()
        return self

    def get_selected_slot(self) -> int:
        """
        Return the selected slot of the hotbar.
        """
        return self._selected_slot

    def get_selected_slot_item(self) -> Item:
        """
        Return the item of the selected hotbar slot.
        """
        return self._slots[self._selected_slot].get_item()

    def get_slot(self, slot_index: int) -> Slot:
        """
        Return the slot object of the hotbar at specified index.
        """
        return self._slots[slot_index]

    def get_slots(self) -> list[Slot]:
        """
        Return all hotbar slots.
        """
        return self._slots

    def set_atlas(self, atlas: Surface) -> Self:
        """
        Set the texture atlas that will be used by the hotbar, then return the hotbar itself.
        """
        self._atlas = atlas
        return self

    def get_atlas(self) -> Surface:
        """
        Return the texture atlas used by the hotbar.
        """
        return self._atlas
