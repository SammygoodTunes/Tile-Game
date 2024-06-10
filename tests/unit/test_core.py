"""
Tests dedicated to the core modules.
"""

from pygame import Rect
from pygame.display import init as init_display, get_caption, quit
from pygame.font import init as init_font

from game.core.game import Game
from game.core.window import Window

WINDOW_TEST_WIDTH = 800
WINDOW_TEST_HEIGHT = 600


def test_window_creation():
    """
    Test: window_creation
    Desc: Tests if the window is created correctly.
    """
    init_display()
    init_font()
    new_window = Window(WINDOW_TEST_WIDTH, WINDOW_TEST_HEIGHT, title='Dummy window')
    assert isinstance(new_window, Window)
    assert new_window.width == WINDOW_TEST_WIDTH
    assert new_window.height == WINDOW_TEST_HEIGHT
    assert new_window.screen.get_rect() == Rect(0, 0, WINDOW_TEST_WIDTH, WINDOW_TEST_HEIGHT)
    assert new_window.font is not None
    assert get_caption()[0] == 'Dummy window'
    quit()


def test_window_fullscreen():
    """
    Test: window_fullscreen
    Desc: Tests if the fullscreen feature of the window is working correctly.
    """
    init_display()
    init_font()
    new_window = Window(WINDOW_TEST_WIDTH, WINDOW_TEST_HEIGHT)
    old_width, old_height = new_window.width, new_window.height
    new_window.toggle_fullscreen()
    assert new_window.fullscreen
    assert new_window.width == new_window.max_width
    assert new_window.height == new_window.max_height
    assert new_window.old_width == old_width
    assert new_window.old_height == old_height
    new_window.toggle_fullscreen()
    assert not new_window.fullscreen
    assert new_window.width == old_width
    assert new_window.height == old_height
    quit()


def test_game_creation():
    """
    Test: game_creation
    Desc: Tests if the game object is instantiated correctly.
    """
    init_display()
    init_font()
    new_game = Game(WINDOW_TEST_WIDTH, WINDOW_TEST_HEIGHT)
    assert isinstance(new_game, Window) and isinstance(new_game, Game)
    assert new_game.client.camera is not None
    assert new_game.client.player is not None
    assert new_game.client.world is not None
    new_game.stop()
    assert not new_game.is_running()
    quit()
