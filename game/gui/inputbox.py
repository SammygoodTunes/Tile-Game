
from pygame import mouse, draw, event, key, MOUSEBUTTONDOWN, KEYDOWN, K_BACKSPACE, K_RETURN, Surface, BLEND_ALPHA_SDL2
from pygame.math import clamp
from string import printable, digits, ascii_letters
from typing import Self

from game.gui.label import Widget, Label
from game.data.states import MouseStates
from game.utils.logger import logger


class InputBox(Widget):
    """
    Class for creating an input box.
    """

    MIN_WIDTH = 25
    MAX_WIDTH = 800
    MIN_HEIGHT = 25
    MAX_HEIGHT = 50

    def __init__(self, text: str = "", placeholder: str = "", x: int = 0, y: int = 0, width: int = 200, height: int = 50) -> None:
        super().__init__(x, y)
        self._width = width
        self._height = height
        self._selected = False
        self._border_colour = (255, 255, 255)
        self._background_colour = (0, 0, 0)
        self._cursor_colour = (190, 255, 10)
        self._text_value = text
        self._text_offset = 0
        self._order = 0
        self._max_text_length = 64
        self._authorised_chars = printable[:-5]
        self._placeholder_label = Label(placeholder, 5, 0).set_font_sizes((8, 10, 12)).set_colour((225, 225, 225)).set_transparency(0.5)
        self._text_label = Label(self._text_value, 5, 0).set_font_sizes((8, 10, 12))
        logger.debug(f'Created {__class__.__name__} with attributes {self.__dict__}')

    def draw(self, screen: Surface) -> None:
        """
        Draw the input box and its components.
        """
        background_surface = Surface((self._width, self._height))
        background_surface.set_alpha(128)
        draw.rect(background_surface, self._background_colour, (self._x, self._y, self._width, self._height))
        screen.blit(background_surface, (self._x, self._y), special_flags=BLEND_ALPHA_SDL2)
        draw.rect(screen, self._border_colour, (self._x, self._y, self._width, self._height), 2)
        if self._text_value.strip():
            self._text_label.draw(screen)
        elif not self._text_value.strip() and self._placeholder_label.get_total_width() < self._width - 10:
            self._placeholder_label.draw(screen)
        if self._selected:
            draw.rect(screen, self._cursor_colour, (
                self._x + self._text_label.get_total_width() + 4, self._y + 8,
                2, self._height - 16))

    def events(self, e: event.Event) -> None:
        """
        Track the input box events.
        """
        if e.type == MOUSEBUTTONDOWN:
            if e.button == MouseStates.LMB:
                self._selected = self.is_hovering_over()
        if e.type == KEYDOWN and self._selected:
            if key.get_pressed()[K_BACKSPACE]:
                self._text_value = self._text_value[:-1]
                if self._text_offset > 0:
                    self._text_offset -= 1
            elif e.unicode in self._authorised_chars and e.unicode.isascii() and len(self._text_value) < self._max_text_length:
                self._text_value += e.unicode
            self.scroll_text()
            self._text_label.set_text(self._text_value[self._text_offset:])

    def update(self, window) -> None:
        """
        Update the input box and its components.
        """
        self._width = int(clamp(window.width * 0.4, InputBox.MIN_WIDTH, InputBox.MAX_WIDTH))
        self._height = int(clamp(window.height * 0.1, InputBox.MIN_HEIGHT, InputBox.MAX_HEIGHT))
        self.scroll_text()
        self._text_label.set_text(self._text_value[self._text_offset:])
        self._placeholder_label.set_auto_font_size(window.width, window.height, window.max_width, window.max_height)
        self._placeholder_label.center_vertically(self._y, self._height)
        self._placeholder_label.set_x(self._x + 5)
        self._text_label.set_auto_font_size(window.width, window.height, window.max_width, window.max_height)
        self._text_label.center_vertically(self._y, self._height)
        self._text_label.set_x(self._x + 5)
        self.refresh()

    def refresh(self) -> None:
        """
        Refresh the input box and its components.
        """
        self._placeholder_label.refresh()
        self._text_label.refresh()

    def scroll_text(self):
        """
        Internal method for calculating how and when to scroll text when going beyond the input box.
        I am aware of how awful it is. Why? because O(n).
        What does that mean? the larger the text, the slower it gets! Very bad!
        Might not be that noticeable for small strings, but still...
        TODO: Make it better, fool.
        """
        diff = self._text_label.font.size(self._text_value)[0] - (self._width - 10)
        value = 0
        if diff > 0 or (diff < 0 < self._text_offset):
            for i, _ in enumerate(self._text_value):
                value += self._text_label.font.size(self._text_value[i])[0]
                if value >= diff + 10:
                    self._text_offset = i
                    break

    def authorise_only_ascii(self):
        """
        Authorise only ASCII characters in the input box, then return the input box itself.
        """
        self._authorised_chars = printable[:-5]
        return self

    def authorise_only_numeric(self):
        """
        Authorise only numerical values (0-9) in the input box, then return the input box itself.
        """
        self._authorised_chars = digits
        return self

    def authorise_only_alnum(self):
        """
        Authorise only alphanumerical values (a-zA-Z0-9), then return the input box itself.
        """
        self._authorised_chars = ascii_letters + digits
        return self

    def authorise_only_alnumlines(self):
        """
        Authorise only alphanumerical values (a-zA-Z0-9-_), then return the input box itself.
        This includes dashes (hyphens) and underscores.
        """
        self._authorised_chars = ascii_letters + digits + '-_'
        return self

    def is_hovering_over(self) -> bool:
        """
        Return whether the user's mouse cursor is hovering over the input box or not.
        """
        mouse_x, mouse_y = mouse.get_pos()
        return (self._x <= mouse_x <= self._x + self._width and
                self._y <= mouse_y <= self._y + self._height and self._enabled)

    def set_selected(self, state) -> Self:
        """
        Set the selected state of the input box, then return the input box itself.
        """
        self._selected = state
        return self

    def is_selected(self) -> bool:
        """
        Return whether the input box is selected or not.
        """
        return self._selected

    def center_horizontally(self, parent_x: int, parent_width: int) -> Self:
        """
        Center the input box horizontally relative to the specified parent, then return the input box itself.
        """
        self._x = round(parent_x + parent_width / 2 - self._width / 2)
        self.refresh()
        return self

    def center_vertically(self, parent_y: int, parent_height: int) -> Self:
        """
        Center the input box vertically relative to the specified parent, then return the input box itself.
        """
        self._y = round(parent_y + parent_height / 2 - self._height / 2)
        self.refresh()
        return self

    def center(self, parent_x: int, parent_y: int, parent_width: int, parent_height: int) -> Self:
        """
        Center the input box on both axes relative to the specified parent, then return the input box itself.
        """
        self.center_horizontally(parent_x, parent_width).center_vertically(parent_y, parent_height)
        return self

    def center_with_offset(self, parent_x: int, parent_y: int, parent_width: int, parent_height: int, x: int, y: int) -> Self:
        """
        Center the input box with center() and offset it by x and y relative to the specified parent, then return the
        input box itself.
        """
        self.center(parent_x, parent_y, parent_width, parent_height).offset(x, y)
        return self

    def set_width(self, width: int) -> Self:
        """
        Set the width of the input box, then return the input box itself.
        """
        self._width = width
        return self

    def get_width(self) -> int:
        """
        Return the width of the input box.
        """
        return self._width

    def set_height(self, height: int) -> Self:
        """
        Set the height of the input box, then return the input box itself.
        """
        self._height = height
        return self

    def get_height(self) -> int:
        """
        Return the height of the input box.
        """
        return self._height

    def set_border_colour(self, border_colour: tuple[int, int, int]) -> Self:
        """
        Set the border colour of the input box, then return the input box itself.
        """
        self._border_colour = border_colour
        return self

    def get_border_colour(self) -> tuple[int, int, int]:
        """
        Return the border colour of the input box.
        """
        return self._border_colour

    def set_background_colour(self, background_colour: tuple[int, int, int]) -> Self:
        """
        Set the background colour of the input box, then return the input box itself.
        """
        self._background_colour = background_colour
        return self

    def get_background_colour(self) -> tuple[int, int, int]:
        """
        Return the background colour of the input box.
        """
        return self._background_colour

    def set_cursor_colour(self, cursor_colour: tuple[int, int, int]) -> Self:
        """
        Set the cursor colour of the input box, then return the input box itself.
        """
        self._cursor_colour = cursor_colour
        return self

    def get_cursor_colour(self) -> tuple[int, int, int]:
        """
        Return the cursor colour of the input box.
        """
        return self._cursor_colour

    def set_placeholder_text(self, placeholder_text: str) -> Self:
        """
        Set the placeholder label text of the input box, then return the input box itself.
        """
        self._placeholder_label.set_text(placeholder_text)
        return self

    def get_placeholder_text(self) -> str:
        """
        Return the placeholder label text.
        """
        return self._placeholder_label.get_text()

    def set_text(self, text: str) -> Self:
        """
        Set the label text of the input box, then return the input box itself.
        """
        self._text_value = text
        return self

    def get_text(self) -> str:
        """
        Return the label text of the input box.
        """
        return self._text_value

    def set_max_text_length(self, max_text_length: int) -> Self:
        """
        Set the input box's max text length, then return the input box itself.
        """
        self._max_text_length = max_text_length
        return self

    def get_max_text_length(self) -> int:
        """
        Return the input box's max text length.
        """
        return self._max_text_length

    def set_order(self, order: int) -> Self:
        """
        Set the order of the input box, then return the input box itself.
        Used for tabbing between them.
        """
        self._order = order
        return self

    def get_order(self) -> int:
        """
        Return the order of the input box.
        """
        return self._order
