
class Widget:

    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._colour = (255, 255, 255)
        self._enabled = False

    def set_x(self, x):
        self._x = x
        return self

    def get_x(self):
        return self._x

    def set_y(self, y):
        self._y = y
        return self

    def get_y(self):
        return self._y

    def offset_x(self, offset_x):
        self._x += offset_x
        return self

    def offset_y(self, offset_y):
        self._y += offset_y
        return self

    def offset(self, offset_x, offset_y):
        self._x += offset_x
        self._y += offset_y
        return self

    def set_state(self, state):
        self._enabled = state
        return self

    def get_state(self):
        return self._enabled
