"""
Module name: tiles

This module defines the different map tiles.
"""

from game.data.tiles.tile import Tile


class Tiles:
    """
    Class for creating a collection of tiles.
    """

    VOID: Tile = Tile(0, 0)
    GRASS: Tile = Tile(1, 0)
    PLAINS: Tile = Tile(2, 0)
    DIRT: Tile = Tile(3, 0)
    COBBLESTONE: Tile = Tile(4, 0).set_resistance(10)
    SAND: Tile = Tile(5, 0)
    COBBLESTONE_STAIRS: Tile = Tile(6, 0)
    FIRESTONE: Tile = Tile(7, 0)
    WATER: Tile = Tile(0, 1)
    LAVA: Tile = Tile(1, 1).set_damage(3).set_damage_delay(0.5)
    BREAK_TILES_ANIM: tuple[Tile] = tuple(Tile(x, 7) for x in range(8))
