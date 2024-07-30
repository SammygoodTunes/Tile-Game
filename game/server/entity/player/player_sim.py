
from game.data.properties import PlayerProperties
from game.data.states import PlayerStates


def calculate_new_pos(position: tuple[float, float], direction: int, delta: float) -> tuple[float, float]:
    print(f'{position=}, {direction=}, {delta=}')
    x, y = position
    if bool(1 & direction >> PlayerStates.MOVE_LEFT):
        x -= round(PlayerProperties.SPEED * delta, 2)
    if bool(1 & direction >> PlayerStates.MOVE_RIGHT):
        x += round(PlayerProperties.SPEED * delta, 2)
    if bool(1 & direction >> PlayerStates.MOVE_UP):
        y -= round(PlayerProperties.SPEED * delta, 2)
    if bool(1 & direction >> PlayerStates.MOVE_DOWN):
        y += round(PlayerProperties.SPEED * delta, 2)
    return x, y
