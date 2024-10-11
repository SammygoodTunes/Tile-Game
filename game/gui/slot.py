
from pygame import Surface, SRCALPHA, image
from pygame.draw import rect
from pygame.math import clamp
from pygame.transform import scale
from typing import Self

from game.data.items.items import Items
from game.data.items.item import Item
from game.gui.widget import Widget
from game.world.item_manager import ItemManager
from game.utils.logger import logger


class Slot(Widget):
    """
    Class for creating a slot.
    """

    MIN_SIZE = 25
    MAX_SIZE = 75

    def __init__(self, x: int = 0, y: int = 0) -> None:
        super().__init__(x, y)
        self._width = 64
        self._height = 64
        self._outline_colour = (25, 25, 25)
        self._inner_colour = (255, 255, 255)
        self._fill_colour = (124, 102, 210)
        self._outline_width = 3
        self._inner_width = 3
        self._fill_alpha = 100
        self._fill_surface = Surface((self._width - 4, self._height - 4), SRCALPHA, 32).convert_alpha()
        self._item: Item | None = None
        self._item_asset: Surface | None = None
        self._item_count = 0
        self._selected = False
        self.set_item(Items.AIR)


    def draw(self, screen) -> None:
        """
        Draw the slot and its components.
        """
        fill_colour = (60, 40, 210) if self._selected else self._fill_colour
        inner_colour = self._inner_colour if self._selected else (128, 128, 128)
        self._fill_surface.fill(fill_colour, (0, 0, self._width - 4, self._height - 4))
        self._fill_surface.set_alpha(self._fill_alpha)
        screen.blit(self._fill_surface, (self._x + 2, self._y + 2, self._width - 4, self._height - 4))

        if self._item_asset is not None:
            item_asset = scale(self._item_asset, (self._width - 12, self._height - 12))
            screen.blit(item_asset, (self._x + 4, self._y + 4, self._width, self._height))

        rect(screen, self._outline_colour, (self._x, self._y, self._width, self._height), self._outline_width, 4)
        rect(screen, inner_colour, (
                                        self._x + self._outline_width - 1,
                                        self._y + self._outline_width - 1,
                                        self._width - self._outline_width - 1,
                                        self._height - self._outline_width - 1
                                    ), self._inner_width, 4)
        rect(screen, self._outline_colour, (
                                                self._x + self._outline_width - 1 + self._inner_width - 1,
                                                self._y + self._outline_width - 1 + self._inner_width - 1,
                                                self._width - self._outline_width - 1 - self._inner_width - 1,
                                                self._height - self._outline_width - 1 - self._inner_width - 1
                                            ), self._outline_width, 4)

    def update(self, window) -> Self:
        """
        Update the slot and its components.
        """
        self._width = self._height = clamp(window.width * 0.12, Slot.MIN_SIZE, Slot.MAX_SIZE)
        self._fill_surface = Surface((self._width, self._height), SRCALPHA, 32).convert_alpha()
        return self

    def center_horizontally(self, parent_x: int, parent_width: int) -> Self:
        """
        Center the slot horizontally relative to the specified parent, then return the slot itself.
        """
        self._x = round(parent_x + parent_width / 2 - self._width / 2)
        return self

    def center_vertically(self, parent_y: int, parent_height: int) -> Self:
        """
        Center the slot vertically relative to the specified parent, then return the slot itself.
        """
        self._y = round(parent_y + parent_height / 2 - self._height / 2)
        return self

    def select(self) -> Self:
        """
        Select the slot, then return the slot itself.
        """
        self._selected = True
        return self

    def unselect(self) -> Self:
        """
        Unselect the slot, then return the slot itself.
        """
        self._selected = False
        return self

    def is_selected(self) -> bool:
        """
        Return whether the slot is selected or not.
        """
        return self._selected

    def set_width(self, width: int) -> Self:
        """
        Set the width of the slot, then return the slot itself.
        """
        self._width = width
        return self

    def get_width(self) -> int:
        """
        Return the width of the slot.
        """
        return self._width

    def set_height(self, height: int) -> Self:
        """
        Set the height of the slot, then return the slot itself.
        """
        self._height = height
        return self

    def get_height(self) -> int:
        """
        Return the height of the slot.
        """
        return self._height

    def set_inner_colour(self, inner_colour: tuple[int, int, int]) -> Self:
        """
        Set the inner colour of the slot, then return the slot itself.
        """
        self._inner_colour = inner_colour
        return self

    def get_inner_colour(self) -> tuple[int, int, int]:
        """
        Return the inner colour of the slot.
        """
        return self._inner_colour

    def set_outline_colour(self, outline_colour: tuple[int, int, int]) -> Self:
        """
        Set the outline colour of the slot, then return the slot itself.
        """
        self._outline_colour = outline_colour
        return self

    def get_outline_colour(self) -> tuple[int, int, int]:
        """
        Return the outline colour of the slot.
        """
        return self._outline_colour

    def set_inner_width(self, inner_width: int) -> Self:
        """
        Set the inner width of the slot, then return the slot itself.
        """
        self._inner_width = inner_width
        return self

    def get_inner_width(self) -> int:
        """
        Return the inner width of the slot.
        """
        return self._inner_width

    def set_outline_width(self, outline_width: int) -> Self:
        """
        Return the outline width of the slot.
        """
        self._outline_width = outline_width
        return self

    def get_outline_width(self) -> int:
        """
        Return the outline width of the slot.
        """
        return self._outline_width

    def set_item(self, item: Item) -> Self:
        """
        Set the item of the slot, then return the slot itself.
        """
        self._item = item
        self._item_asset = Surface((ItemManager.SIZE, ItemManager.SIZE), SRCALPHA, 32).convert_alpha()
        self._item_asset.blit(image.load(Item.DEFAULT_ATLAS).convert_alpha(), (0, 0, ItemManager.SIZE, ItemManager.SIZE),
                    (ItemManager.SIZE * item.get_xy()[0], ItemManager.SIZE * item.get_xy()[1], ItemManager.SIZE, ItemManager.SIZE))
        return self

    def get_item(self) -> Item:
        """
        Return the item of the slot.
        """
        return self._item

    def get_item_asset(self) -> Surface:
        """
        Return the item asset of the slot.
        """
        return self._item_asset

    def clear_item_asset(self) -> Self:
        """
        Clear the item asset of the slot, then return the slot itself.
        """
        self._item_asset = None
        return self
