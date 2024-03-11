
'''
Tests dedicated to the core module.
'''

from pygame.display import init as init_display, get_caption
from pygame.font import init as init_font
from pygame import Rect

from game.core.window import Window
from game.core.game import Game
from game.data.data_manager import get_game_property, APP_NAME

WINDOW_TEST_WIDTH = 800
WINDOW_TEST_HEIGHT = 600


def test_window_creation():
    init_display()
    init_font()
    new_window = Window(WINDOW_TEST_WIDTH, WINDOW_TEST_HEIGHT)
    assert new_window.width == WINDOW_TEST_WIDTH
    assert new_window.height == WINDOW_TEST_HEIGHT
    assert new_window.screen.get_rect() == Rect(0, 0, WINDOW_TEST_WIDTH, WINDOW_TEST_HEIGHT)
    assert new_window.font is not None
    assert get_caption()[0] == get_game_property(APP_NAME)


def test_game_creation():
    init_display()
    init_font()
    new_game = Game(WINDOW_TEST_WIDTH, WINDOW_TEST_HEIGHT)
    assert new_game.camera is not None
    assert new_game.player is not None
    assert new_game.world is not None
    new_game.stop()
    assert new_game.is_running() == False
