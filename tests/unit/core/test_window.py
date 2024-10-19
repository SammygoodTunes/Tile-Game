"""
Tests dedicated to the window module.
"""

from pygame import Rect
from pygame.display import init as init_display, quit
from pygame.font import init as init_font

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
    new_window = Window(WINDOW_TEST_WIDTH, WINDOW_TEST_HEIGHT)
    assert isinstance(new_window, Window)
    assert new_window.width == WINDOW_TEST_WIDTH
    assert new_window.height == WINDOW_TEST_HEIGHT
    assert new_window.screen.get_rect() == Rect(0, 0, WINDOW_TEST_WIDTH, WINDOW_TEST_HEIGHT)
    assert new_window.font is not None
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