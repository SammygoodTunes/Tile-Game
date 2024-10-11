
class PlayerProperties:
    """
    Class for player properties.
    """

    MAX_PLAYER_NAME_SIZE = 16
    SPEED = 350
    SPEED_IN_WATER = SPEED // 2
    SPEED_IN_LAVA = SPEED // 3
    TEXTURE: str = 'game/assets/player.png'
    VELOCITY_START_DURATION: float = 0.25
    VELOCITY_STOP_DURATION: float = 0.25
    VELOCITY_THRESHOLD: float = 0.0001
