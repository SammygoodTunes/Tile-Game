"""
Module name: themes

This module defines the different world themes.
"""
from game.data.themes.theme import Theme
from game.data.themes.theme_layers import ThemeLayers
from game.data.tiles.tiles import Tiles


class Themes:
    """
    Class for creating a collection of world themes.
    """

    DEFAULT: Theme = (
        Theme('Default')
        .add_layer(ThemeLayers.LAYER_B, 0, -1500, Tiles.WATER)
        .add_layer(ThemeLayers.LAYER_C, -1500, -1000, Tiles.SAND)
        .add_layer(ThemeLayers.LAYER_C, -1000, -600, Tiles.DIRT)
        .add_layer(ThemeLayers.LAYER_C, -600, -300, Tiles.PLAINS)
        .add_layer(ThemeLayers.LAYER_C, -300, 100, Tiles.GRASS)
        .add_layer(ThemeLayers.LAYER_C, 100, 500, Tiles.PLAINS)
        .add_layer(ThemeLayers.LAYER_C, 500, 2000, Tiles.COBBLESTONE)
        .add_layer(ThemeLayers.LAYER_T, 2000, 0, Tiles.LAVA)
    )

    HELL: Theme = (
        Theme('Hell')
        .add_layer(ThemeLayers.LAYER_B, 0, -1500, Tiles.LAVA)
        .add_layer(ThemeLayers.LAYER_C, -1500, -1000, Tiles.SAND)
        .add_layer(ThemeLayers.LAYER_C, -1000, -300, Tiles.DIRT)
        .add_layer(ThemeLayers.LAYER_C, -300, 100, Tiles.COBBLESTONE)
        .add_layer(ThemeLayers.LAYER_C, 100, 500, Tiles.DIRT)
        .add_layer(ThemeLayers.LAYER_C, 500, 2000, Tiles.FIRESTONE)
        .add_layer(ThemeLayers.LAYER_T, 2000, 0, Tiles.LAVA)
    )

    ISLANDS: Theme = (
        Theme('Islands')
        .add_layer(ThemeLayers.LAYER_B, 0, -1500, Tiles.WATER)
        .add_layer(ThemeLayers.LAYER_C, -1500, -1150, Tiles.SAND)
        .add_layer(ThemeLayers.LAYER_C, -1150, -1000, Tiles.DIRT)
        .add_layer(ThemeLayers.LAYER_C, -1000, -900, Tiles.PLAINS)
        .add_layer(ThemeLayers.LAYER_C, -900, -800, Tiles.GRASS)
        .add_layer(ThemeLayers.LAYER_C, -800, -650, Tiles.PLAINS)
        .add_layer(ThemeLayers.LAYER_C, -650, -475, Tiles.COBBLESTONE)
        .add_layer(ThemeLayers.LAYER_C, -475, -350, Tiles.PLAINS)
        .add_layer(ThemeLayers.LAYER_C, -350, -200, Tiles.DIRT)
        .add_layer(ThemeLayers.LAYER_C, -200, 0, Tiles.SAND)
        .add_layer(ThemeLayers.LAYER_T, 0, 0, Tiles.WATER)
    )
