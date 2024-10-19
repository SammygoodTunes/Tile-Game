"""
Module name: tiles

This module defines the different map tiles.
"""

from game.data.tiles.tile import Tile


class Tiles:
    """
    Class for creating a collection of tiles.
    """

    VOID: Tile = Tile()
    GRASS: Tile = Tile(x=1)
    PLAINS: Tile = Tile(x=2)
    DIRT: Tile = Tile(x=3)
    COBBLESTONE: Tile = Tile(x=4).set_resistance(10)
    SAND: Tile = Tile(x=5)
    COBBLESTONE_STAIRS: Tile = Tile(x=6)
    FIRESTONE: Tile = Tile(x=7)
    WATER: Tile = Tile(y=1)
    LAVA: Tile = Tile(x=1, y=1).set_damage(3).set_damage_delay(0.5)
    BREAK_TILES_ANIM: tuple[Tile] = tuple(Tile(x=x, y=7) for x in range(8))
