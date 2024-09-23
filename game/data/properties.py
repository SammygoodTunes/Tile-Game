
from importlib import resources as impr


class PlayerProperties:
    """
    Class for player properties.
    """

    MAX_PLAYER_NAME_SIZE = 16
    SPEED = 350
    SPEED_IN_WATER = SPEED // 2
    SPEED_IN_LAVA = SPEED // 3
    TEXTURE: str = str(impr.files('assets') / "player.png")
    VELOCITY_START_DURATION: float = 0.25
    VELOCITY_STOP_DURATION: float = 0.25
    VELOCITY_THRESHOLD: float = 0.0001


class CameraProperties:
    """
    Class for camera properties.
    """

    SPEED = 350
    VELOCITY_START_DURATION: float = 0.25
    VELOCITY_STOP_DURATION: float = 0.5


class ScreenProperties:
    """
    Class for screen properties.
    """

    ALPHA = 128
    PRONOUNCED_ALPHA = 160


class ServerProperties:
    """
    Class for server properties.
    """

    TICKS_PER_SECOND = 20
    MAX_PLAYERS = 10


class WorldProperties:
    """
    Class for world properties.
    """

    SKY_COLOUR = (140, 150, 235)
