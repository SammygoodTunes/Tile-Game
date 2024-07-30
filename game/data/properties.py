
from importlib import resources as impr


class PlayerProperties:
    """
    Class for player properties.
    """

    MAX_PLAYER_NAME_SIZE = 16
    SPEED = 350
    TEXTURE: str = str(impr.files('assets') / "player.png")
    VELOCITY_STEP_START: float = 4.5
    VELOCITY_STEP_STOP: float = 5.0


class CameraProperties:
    """
    Class for camera properties.
    """

    SPEED = 350


class ScreenProperties:
    """
    Class for screen properties.
    """

    ALPHA = 128


class ServerProperties:
    """
    Class for server properties.
    """

    TICKS_PER_SECOND = 20


class WorldProperties:
    """
    Class for world properties.
    """

    SKY_COLOUR = (140, 150, 235)
