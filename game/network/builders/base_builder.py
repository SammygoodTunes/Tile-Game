
class BaseBuilder:
    """
    Base class for packet building
    """
    COMMAND_ID_KEY = 'id'
    TIMESTAMP_KEY = 'timestamp'

    COMMAND_ID_MAX = 1
    COMMAND_ID_RANGE = range(0, COMMAND_ID_MAX + 1)
    COMMAND_ID_OFFSET = 0x1d

    (
        PLAYER_POSITION_UPDATE_COMMAND,
        PLAYER_TILE_BREAK_COMMAND,
    ) = COMMAND_ID_RANGE
