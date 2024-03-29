
from game.utils.logger import logger


class Screen:

    def __init__(self):
        self._enabled = False
        logger.debug(f'Created {__class__.__name__} with attributes {self.__dict__}')

    def set_state(self, state):
        self._enabled = state

    def get_state(self):
        return self._enabled
