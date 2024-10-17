"""
Module name: exceptions

Defines certain specific exceptions that may be raised during or before the game.
This module may disappear in the future.
"""

class InvalidTextureAtlas(Exception):
    """
    Class for creating the exception caused by loading an invalid texture atlas.
    """

    def __init__(self, message="Invalid texture atlas, have you loaded one with set_atlas()?") -> None:
        super().__init__(message)


class InvalidMapData(Exception):
    """
    Class for creating the exception caused by invalid map data.
    """

    def __init__(self, message="Invalid map data, have you initialise the map with initialise()?") -> None:
        super().__init__(message)


class OutOfMapBounds(Exception):
    """
    Class for creating the exception caused by overflowing the map data array.
    """

    def __init__(self, message="Out of map boundaries, make sure to stay within them!") -> None:
        super().__init__(message)


class InvalidGamePropertyValue(Exception):
    """
    Class for creating the exception caused by an invalid game property value.
    """

    def __init__(self, message):
        super().__init__(f'Invalid game property value, expected: {message}')


class ZeroOrLessSpawnPlayerAttempts(Exception):
    """
    Class for creating the exception caused by setting the number of attempts to zero or less when finding an ideal
    spawn point for the player.
    """

    def __init__(self, message="Number of attempts to choose player spawn point must be at least 1."):
        super().__init__(message)


class PlayerNameAlreadyExists(Exception):
    """
    Class for creating the exception caused by joining a server with an in-game name that is already taken.
    """

    def __init__(self, message="Your current player name is already taken, please change it."):
        super().__init__(message)


class MaxPlayersReached(Exception):
    """
    Class for creating the exception caused by reaching the maximum player count of a server.
    """

    def __init__(self, message="The player number limit has been reached, please come back later."):
        super().__init__(message)
