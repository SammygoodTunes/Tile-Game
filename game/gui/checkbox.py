
from pygame.draw import rect as draw_rect
from pygame import event, mouse, MOUSEBUTTONDOWN
from typing import Self

from game.data.states.mouse_states import MouseStates
from game.gui.label import Label
from game.gui.widget import Widget
from game.utils.logger import logger


class Checkbox(Widget):
    """
    Class for creating a checkbox.
    """

    def __init__(self, title: str, x: int = 0, y: int = 0, checked: bool = False) -> None:
        super().__init__(x, y)
        self._checked = checked
        self._colour = (255, 255, 255)
        self._size = 20
        self._spacing = 8
        self.title_label = Label(title, self._x + self._size + self._spacing, self._y).set_font_sizes((7, 8, 10))


    def draw(self, screen) -> None:
        """
        Draw the checkbox and its components.
        """
        if self._checked:
            draw_rect(screen, self._colour, (self._x + 4, self._y + 4, self._size - 8, self._size - 8), border_radius=0)
        draw_rect(screen, self._colour, (self._x, self._y, self._size, self._size), width=2, border_radius=2)
        self.title_label.draw(screen)

    def events(self, e: event.Event) -> None:
        """
        Track the checkbox events.
        """
        if e.type == MOUSEBUTTONDOWN:
            if e.button == MouseStates.LMB and self.is_hovering_over():
                self._checked = not self._checked

    def update(self, window) -> None:
        """
        Update the checkbox and its components.
        """
        self.title_label.set_auto_font_size(window.width, window.height, window.max_width, window.max_height)
        self.refresh()

    def refresh(self) -> None:
        """
        Refresh the checkbox and its components.
        """
        width, height = self.title_label.font.size(self.title_label.get_text())
        self.title_label.center_horizontally(width / 2 + self._x + self._size + self._spacing, self._size)
        self.title_label.center_vertically(self._y, self._size)
        self.title_label.refresh()

    def is_hovering_over(self) -> bool:
        """
        Return whether the user's mouse cursor is hovering over the checkbox or not.
        The bounding box of the checkbox includes the button and the text.
        """
        mouse_x, mouse_y = mouse.get_pos()
        width = self.title_label.font.size(self.title_label.get_text())[0]
        return (self._x <= mouse_x <= self._x + self._size + self._spacing * 2 + width and
                self._y <= mouse_y <= self._y + self._size and self._enabled)

    def center_horizontally(self, parent_x: int, parent_width: int) -> Self:
        """
        Center the checkbox horizontally relative to the specified parent, then return the checkbox itself.
        """
        self._x = round(parent_x + parent_width / 2 - self._size / 2)
        self.refresh()
        return self

    def center_vertically(self, parent_y: int, parent_height: int) -> Self:
        """
        Center the checkbox vertically relative to the specified parent, then return the checkbox itself.
        """
        self._y = round(parent_y + parent_height / 2 - self._size / 2)
        self.refresh()
        return self

    def center(self, parent_x: int, parent_y: int, parent_width: int, parent_height: int) -> Self:
        """
        Center the checkbox on both axes relative to the specified parent, then return the checkbox itself.
        """
        self.center_horizontally(parent_x, parent_width).center_vertically(parent_y, parent_height)
        return self

    def center_with_offset(self, parent_x: int, parent_y: int, parent_width: int, parent_height: int, x: int, y: int) -> Self:
        """
        Center the checkbox with center() and offset it by x and y relative to the specified parent, then return the
        checkbox itself.
        """
        self.center(parent_x, parent_y, parent_width, parent_height).offset(x, y)
        self.refresh()
        return self

    def set_size(self, size: int) -> Self:
        """
        Set the size of the checkbox's button, then return the checkbox itself.
        """
        self._size = size
        return self

    def get_size(self) -> int:
        """
        Return the size of the checkbox's button.
        """
        return self._size

    def set_checked(self, state: bool) -> Self:
        """
        Set the checked state of the checkbox's button, then return the checkbox itself.
        """
        self._checked = state
        return self

    def is_checked(self) -> bool:
        """
        Return the checked state of the checkbox's button.
        """
        return self._checked

    def offset_x(self, offset_x: int) -> Self:
        """
        Offset the checkbox on the x-axis, then return the checkbox itself.
        """
        super().offset_x(offset_x)
        self.title_label.set_x(self.title_label.get_x() + offset_x)
        self.title_label.set_shadow_x_offset(2)
        return self

    def offset_y(self, offset_y: int) -> Self:
        """
        Offset the checkbox on the y-axis, then return the checkbox itself.
        """
        super().offset_y(offset_y)
        self.title_label.set_y(self.title_label.get_y() + offset_y)
        self.title_label.set_shadow_y_offset(2)
        return self
