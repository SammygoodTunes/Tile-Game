
from importlib import resources as impr


class PlayerProperties:
    """
    Class for player properties.
    """

    MAX_PLAYER_NAME_SIZE = 16
    SPEED = 350
    SPEED_IN_WATER = SPEED // 2
    SPEED_IN_LAVA = SPEED // 3
    TEXTURE: str = "assets/player.png"
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
    MAX_MAP_WIDTH = 256
    MAX_MAP_HEIGHT = 256

class TileProperties:
    """
    Class for tile properties.
    """

    TILE_ID_MAX = 63
    TILE_X_MAX = 7
    TILE_Y_MAX = 7
    TILE_RESISTANCE_MAX = 63
    TILE_DAMAGE_MAX = 127
    TILE_DAMAGE_DELAY_MAX = 0.8 * 10
