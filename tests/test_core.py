
'''
Tests dedicated to the assets.
'''

from pygame.display import get_caption

from game.core.window import Window
from game.core.game import Game
from game.data.data_manager import get_game_property, APP_NAME

WINDOW_TEST_WIDTH = 800
WINDOW_TEST_HEIGHT = 600

def test_window_creation():
    new_window = Window(WINDOW_TEST_WIDTH, WINDOW_TEST_HEIGHT)
    assert new_window.width == WINDOW_TEST_WIDTH
    assert new_window.height == WINDOW_TEST_HEIGHT
    assert new_window.screen.get_rect() == (WINDOW_TEST_WIDTH, WINDOW_TEST_HEIGHT)
    assert new_window.font is not None
    assert get_caption() == get_game_property(APP_NAME)
