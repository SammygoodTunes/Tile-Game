"""
Tests dedicated to the game module.
"""

from pygame.display import init as init_display, quit
from pygame.font import init as init_font

from game.core.game import Game
from game.core.window import Window

WINDOW_TEST_WIDTH = 800
WINDOW_TEST_HEIGHT = 600


def test_game_creation():
    """
    Test: game_creation
    Desc: Tests if the game object is instantiated correctly.
    Rqmt: The attributes must not be None and the running attribute must be False on game termination.
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
