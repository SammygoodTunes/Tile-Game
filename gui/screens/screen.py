
class Screen:

    def __init__(self):
        self._enabled = False

    def set_state(self, state):
        self._enabled = state

    def get_state(self):
        return self._enabled
