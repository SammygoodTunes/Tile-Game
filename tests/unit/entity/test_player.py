"""
Tests dedicated to the player module.
"""

from game.entity.player import Player
from game.data.states.player_states import PlayerStates


def test_player_creation():
    """
    Test: player_creation
    Desc: Tests if the player is instantiated correctly.
    Rqmt: The attributes must be equaled to the given values.
    """
    dummy_player = Player(-128, 128, 100)
    assert dummy_player.get_x() == -128
    assert dummy_player.get_y() == 128
    assert dummy_player.speed == 100

def test_player_reset():
    """
    Test: player_reset
    Desc: Tests if the player's general attributes reset correctly.
    Rqmt: The attributes must be equaled to their default value.
    """
    dummy_player = Player(-128, 128, 100)
    dummy_player.velocity_x, dummy_player.velocity_y = 1.0, -1.0
    dummy_player.move = 6
    dummy_player.health = 0
    dummy_player.hurt = True
    dummy_player.reset()
    assert dummy_player.get_x() == dummy_player.get_y() == 0
    assert dummy_player.velocity_x == dummy_player.velocity_y == 0
    assert dummy_player.move == 0
    assert dummy_player.get_health() == 100
    assert not dummy_player.hurt

def test_player_movement():
    """
    Test: player_movement
    Desc: Tests if the player's movement verifiers return the right movement state of the player.
    Rqmt: The player movement methods should return the right boolean state based on the player move attribute.
    """
    dummy_player = Player()
    dummy_player.move |= (1 << PlayerStates.MOVE_LEFT)
    assert (
        dummy_player.is_moving_left() and
        not dummy_player.is_moving_up()
    )
    dummy_player.move |= (1 << PlayerStates.MOVE_UP)
    dummy_player.move &= ~(1 << PlayerStates.MOVE_LEFT)
    assert not (
        dummy_player.is_moving_left() and
        dummy_player.is_moving_up()
    )
    dummy_player.move &= ~(1 << PlayerStates.MOVE_UP)
    dummy_player.move |= (1 << PlayerStates.MOVE_DOWN)
    assert not (
        dummy_player.is_moving_up() and
        dummy_player.is_moving_down()
    )
    dummy_player.move &= ~(1 << PlayerStates.MOVE_DOWN)
    dummy_player.move |= (1 << PlayerStates.MOVE_RIGHT)
    assert not (
            dummy_player.is_moving_up() and
            dummy_player.is_moving_right()
    )
    dummy_player.move &= ~(1 << PlayerStates.MOVE_RIGHT)
    assert (
        not dummy_player.is_moving_up() and
        not dummy_player.is_moving_left() and
        not dummy_player.is_moving_down() and
        not dummy_player.is_moving_right()
    )
    dummy_player.move |= (1 << PlayerStates.MOVE_LEFT)
    dummy_player.move |= (1 << PlayerStates.MOVE_UP)
    dummy_player.move |= (1 << PlayerStates.MOVE_DOWN)
    dummy_player.move |= (1 << PlayerStates.MOVE_RIGHT)
    assert (
        dummy_player.is_moving_up() and
        dummy_player.is_moving_left() and
        dummy_player.is_moving_down() and
        dummy_player.is_moving_right()
    )
