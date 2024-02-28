
from pygame.font import Font
from .widget import Widget


class Label(Widget):
    DEFAULT_FONT = "assets/font.ttf"
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

    def __repr__(self):
        return f"Label at ({self._x, self._y}) with text '{self._text}'"

    def draw(self, screen):
        text_shadow = self.font.render(self._text, self._antialiasing, self._shadow_colour)
        text = self.font.render(self._text, self._antialiasing, self._colour)
        screen.blit(text_shadow, (self._shadow_x, self._shadow_y))
        screen.blit(text, (self._x, self._y))

    def update(self, window):
        self.set_auto_font_size(window.width, window.height, window.max_width, window.max_height)
        self.refresh()

    def refresh(self):
        self._shadow_x = self._x - 2
        self._shadow_y = self._y + 2
        return self

    def center_horizontally(self, parent_x, parent_width):
        width, height = self.font.size(self._text)
        self._x = parent_x + parent_width / 2 - width / 2
        self.refresh()
        return self

    def center_vertically(self, parent_y, parent_height):
        height = self.font.get_height()
        self._y = parent_y + parent_height / 2 - height / 2
        self.refresh()
        return self

    def center(self, parent_x, parent_y, parent_width, parent_height):
        self.center_horizontally(parent_x, parent_width).center_vertically(parent_y, parent_height)
        return self

    def center_with_offset(self, parent_x, parent_y, parent_width, parent_height, x, y):
        self.center(parent_x, parent_y, parent_width, parent_height).offset(x, y)
        self.refresh()
        return self

    def set_auto_font_size(self, width, height, max_width, max_height):
        if width < max_width / 3 and height < max_height / 3:
            self.set_font_size(self._font_sizes[0])
        elif width < max_width / 3 * 2 and height < max_height / 3 * 2:
            self.set_font_size(self._font_sizes[1])
        else:
            self.set_font_size(self._font_sizes[2])
        return self

    def set_font_size(self, font_size):
        self.font = Font(Label.DEFAULT_FONT, font_size)
        self._font_size = font_size
        return self

    def get_font_size(self):
        return self._font_size

    def set_font_sizes(self, font_sizes):
        self._font_sizes = font_sizes
        return self

    def get_font_sizes(self):
        return self._font_sizes

    def get_total_width(self):
        return self.font.size(self._text)[0]

    def get_total_height(self):
        return self.font.size(self._text)[1]

    def set_text(self, text):
        self._text = text
        return self

    def get_text(self):
        return self._text

    def set_antialiasing(self, state):
        self._antialiasing = state
        return self

    def has_antialiasing(self):
        return self._antialiasing

    def set_colour(self, colour):
        self._colour = colour
        return self

    def get_colour(self):
        return self._colour

    def set_shadow_x(self, shadow_x):
        self._shadow_x = shadow_x
        return self

    def set_x(self, x):
        super().set_x(x)
        self.refresh()
        return self

    def set_y(self, y):
        super().set_y(y)
        self.refresh()
        return self

    def get_shadow_x(self):
        return self._shadow_x

    def set_shadow_y(self, shadow_y):
        self._shadow_y = shadow_y
        return self

    def get_shadow_y(self):
        return self._shadow_y

    def set_shadow_x_offset(self, offset):
        self._shadow_x = self._x + offset
        return self

    def set_shadow_y_offset(self, offset):
        self._shadow_y = self._y + offset
        return self

    def set_shadow_colour(self, shadow_colour):
        self._shadow_colour = shadow_colour
        return self

    def get_shadow_colour(self):
        return self._shadow_colour
