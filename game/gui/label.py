
from importlib import resources as impr
from pygame.font import Font

from game import assets
from game.gui.widget import Widget
from game.utils.logger import logger


class Label(Widget):
    """
    Class for creating a label.
    """

    DEFAULT_FONT = impr.files(assets) / "font.ttf"
    DEFAULT_FONT_SIZE_SMALL = 8
    DEFAULT_FONT_SIZE_NORMAL = 11
    DEFAULT_FONT_SIZE_LARGE = 14

    def __init__(self, text="", x=0, y=0):
        super().__init__(x, y)
        self.font = Font(Label.DEFAULT_FONT, Label.DEFAULT_FONT_SIZE_NORMAL)
        self._font_size = Label.DEFAULT_FONT_SIZE_NORMAL
        self._font_sizes = (Label.DEFAULT_FONT_SIZE_SMALL, Label.DEFAULT_FONT_SIZE_NORMAL, Label.DEFAULT_FONT_SIZE_LARGE)
        self._text = text
        self._shadow_x = self._x
        self._shadow_y = self._y
        self._shadow_colour = (0, 0, 0)
        self._antialiasing = False
        logger.debug(f'Created {__class__.__name__} with attributes {self.__dict__}')

    def draw(self, screen):
        """
        Draw the label and its components.
        """
        text_shadow = self.font.render(self._text, self._antialiasing, self._shadow_colour)
        text = self.font.render(self._text, self._antialiasing, self._colour)
        screen.blit(text_shadow, (self._shadow_x, self._shadow_y))
        screen.blit(text, (self._x, self._y))

    def update(self, window):
        """
        Update the label and its components.
        """
        self.set_auto_font_size(window.width, window.height, window.max_width, window.max_height)
        self.refresh()

    def refresh(self):
        """
        Update the shadow's position of the label.
        """
        self._shadow_x = self._x - 2
        self._shadow_y = self._y + 2
        return self

    def center_horizontally(self, parent_x, parent_width):
        """
        Center the label horizontally relative to the specified parent, then return the label itself.
        """
        width, height = self.font.size(self._text)
        self._x = parent_x + parent_width / 2 - width / 2
        self.refresh()
        return self

    def center_vertically(self, parent_y, parent_height):
        """
        Center the label vertically relative to the specified parent, then return the label itself.
        """
        height = self.font.get_height()
        self._y = parent_y + parent_height / 2 - height / 2
        self.refresh()
        return self

    def center(self, parent_x, parent_y, parent_width, parent_height):
        """
        Center the label on both axes relative to the specified parent, then return the label itself.
        """
        self.center_horizontally(parent_x, parent_width).center_vertically(parent_y, parent_height)
        return self

    def center_with_offset(self, parent_x, parent_y, parent_width, parent_height, x, y):
        """
        Center the label with center() and offset it by x and y relative to the specified parent, then return the
        label itself.
        """
        self.center(parent_x, parent_y, parent_width, parent_height).offset(x, y)
        self.refresh()
        return self

    def set_auto_font_size(self, width, height, max_width, max_height):
        """
        Set the automatic font size of the label, then return the label itself.
        """
        if width < max_width / 3 and height < max_height / 3:
            self.set_font_size(self._font_sizes[0])
        elif width < max_width / 3 * 2 and height < max_height / 3 * 2:
            self.set_font_size(self._font_sizes[1])
        else:
            self.set_font_size(self._font_sizes[2])
        return self

    def set_font_size(self, font_size):
        """
        Set the font size of the label, then return the label itself.
        """
        self.font = Font(Label.DEFAULT_FONT, font_size)
        self._font_size = font_size
        return self

    def get_font_size(self):
        """
        Return the font size of the label.
        """
        return self._font_size

    def set_font_sizes(self, font_sizes):
        """
        Set the small, medium and large sizes of the label's text, then return the label itself.
        """
        self._font_sizes = font_sizes
        return self

    def get_font_sizes(self):
        """
        Return the small, medium and large sizes of the label's text.
        """
        return self._font_sizes

    def get_total_width(self):
        """
        Return the total width of the label.
        """
        return self.font.size(self._text)[0]

    def get_total_height(self):
        """
        Return the total height of the label.
        """
        return self.font.size(self._text)[1]

    def set_text(self, text):
        """
        Set the label's text, then return the label itself.
        """
        self._text = text
        return self

    def get_text(self):
        """
        Return the label's text.
        """
        return self._text

    def set_antialiasing(self, state):
        """
        Set the antialiasing state of the label, then return the label itself.
        """
        self._antialiasing = state
        return self

    def has_antialiasing(self):
        """
        Returns True if the label has antialiasing enabled.
        """
        return self._antialiasing

    def set_colour(self, colour):
        """
        Set the label text's foreground colour, then return the label itself.
        """
        self._colour = colour
        return self

    def get_colour(self):
        """
        Return the label text's foreground colour.
        """
        return self._colour

    def set_shadow_x(self, shadow_x):
        """
        Set the label text's shadow's x position, then return the label itself.
        """
        self._shadow_x = shadow_x
        return self

    def set_x(self, x):
        """
        Set the label text's x position, then return the label itself.
        """
        super().set_x(x)
        self.refresh()
        return self

    def set_y(self, y):
        """
        Set the label text's y position, then return the label itself.
        """
        super().set_y(y)
        self.refresh()
        return self

    def get_shadow_x(self):
        """
        Return the label text's shadow's x position.
        """
        return self._shadow_x

    def set_shadow_y(self, shadow_y):
        """
        Set the label text's shadow's y position, then return the label itself.
        """
        self._shadow_y = shadow_y
        return self

    def get_shadow_y(self):
        """
        Return the label text's shadow's y position.
        """
        return self._shadow_y

    def set_shadow_x_offset(self, offset):
        """
        Set the label text's shadow's x offset, then return the label itself.
        """
        self._shadow_x = self._x + offset
        return self

    def set_shadow_y_offset(self, offset):
        """
        Set the label text's shadow's y offset, then return the label itself.
        """
        self._shadow_y = self._y + offset
        return self

    def set_shadow_colour(self, shadow_colour):
        """
        Set the label text's shadow colour, then return the label itself.
        """
        self._shadow_colour = shadow_colour
        return self

    def get_shadow_colour(self):
        """
        Return the label text's shadow colour.
        """
        return self._shadow_colour
