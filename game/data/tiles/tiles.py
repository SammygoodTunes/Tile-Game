"""
Module name: tiles

This module defines the different map tiles.
"""

from game.data.tiles.tile import Tile


class Tiles:
    """
    Class for creating a collection of tiles.
    """

    VOID: Tile = Tile('VOID')
    GRASS: Tile = Tile('GRASS', x=1)
    PLAINS: Tile = Tile('PLAINS', x=2)
    DIRT: Tile = Tile('DIRT', x=3)
    COBBLESTONE: Tile = Tile('COBBLESTONE', x=4).set_resistance(10)
    SAND: Tile = Tile('SAND', x=5)
    COBBLESTONE_STAIRS: Tile = Tile('COBBLESTONE_STAIRS', x=6)
    FIRESTONE: Tile = Tile('FIRESTONE', x=7)
    WATER: Tile = Tile('WATER', y=1)
    LAVA: Tile = Tile('LAVA', x=1, y=1).set_damage(3).set_damage_delay(0.5)
    BREAK_TILES_ANIM: tuple[Tile] = tuple(Tile(f'BREAK_TILE_{x}', x=x, y=7) for x in range(8))
