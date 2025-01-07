"""
Module name: world_properties

This module defines the world properties.
"""

from game.utils.translator import translator as t

class WorldProperties:
    """
    Class for world properties.
    """

    SKY_COLOUR = (140, 150, 235)
    MIN_MAP_WIDTH = 64
    MIN_MAP_HEIGHT = 64
    MAX_MAP_WIDTH = 192
    MAX_MAP_HEIGHT = 192

    MAP_SMALL = 'Small'
    MAP_MEDIUM = 'Medium'
    MAP_LARGE = 'Large'

    @staticmethod
    def translate():
        """
        Translate the world properties.
        """
        WorldProperties.MAP_SMALL = t.t('data.properties.world.map_small')
        WorldProperties.MAP_MEDIUM = t.t('data.properties.world.map_medium')
        WorldProperties.MAP_LARGE = t.t('data.properties.world.map_large')

