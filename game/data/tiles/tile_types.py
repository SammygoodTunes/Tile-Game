"""
Module name: tile_types

This module defines the different types of map tiles.
"""

from game.data.tiles.tiles import Tiles


class TileTypes:
    """
    Class for regrouping tiles into different categories.
    """

    PLACEABLE: tuple[Tiles] = (
        Tiles.VOID,
        Tiles.GRASS,
        Tiles.PLAINS,
        Tiles.DIRT,
        Tiles.COBBLESTONE,
        Tiles.SAND,
        Tiles.WATER,
        Tiles.LAVA,
    )

    BREAKABLE: tuple[Tiles] = (
        Tiles.COBBLESTONE,
        Tiles.FIRESTONE,
    )

    LETHAL: tuple[Tiles] = (
        Tiles.LAVA,
    )
