
from game.data.properties import PlayerProperties
from game.data.states import PlayerStates


def calculate_new_pos(position: tuple[float, float], direction: int, delta: float) -> tuple[float, float]:
    #   0.25 PLAYER START VELOCITY DURATION
    # forcement après la transition: velocity_x/y = 1.0
    # + speed * (delta - 0.25)
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
