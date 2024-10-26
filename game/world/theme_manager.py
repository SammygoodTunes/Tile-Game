"""
Module name: theme_manager

This module manages the world generation theme, as well as generating the default themes JSON file.
"""

from os import path
import json

from game.data.themes.theme import Theme
from game.data.themes.theme_layers import ThemeLayers
from game.data.tiles.tiles import Tiles
from game.utils.logger import logger


class ThemeManager:
    """
    Class for creating the theme manager.
    """

    THEMES_FILE = 'themes.json'

    @staticmethod
    def create_default_themes() -> None:
        """
        Create the default world themes files.
        """
        default_theme = Theme('Default Theme')
        (default_theme
         .add_layer(ThemeLayers.LAYER_B, 0, -1500, Tiles.WATER)
         .add_layer(ThemeLayers.LAYER_C, -1500, -1000, Tiles.SAND)
         .add_layer(ThemeLayers.LAYER_C, -1000, -600, Tiles.DIRT)
         .add_layer(ThemeLayers.LAYER_C, -600, -300, Tiles.PLAINS)
         .add_layer(ThemeLayers.LAYER_C, -300, 100, Tiles.GRASS)
         .add_layer(ThemeLayers.LAYER_C, 100, 500, Tiles.PLAINS)
         .add_layer(ThemeLayers.LAYER_C, 500, 2000, Tiles.COBBLESTONE)
         .add_layer(ThemeLayers.LAYER_T, 2000, 0, Tiles.LAVA))
        json_obj = json.dumps({
            'themes': [
                default_theme.get_dict()
            ]
        }, indent=4)
        with open(ThemeManager.THEMES_FILE, 'w') as theme_file:
            theme_file.write(json_obj)

    @staticmethod
    def check_themes() -> None:
        """
        Check the themes directory and its files.
        """
        if not path.isfile(ThemeManager.THEMES_FILE):
            logger.info('Creating themes file as none were found.')
            ThemeManager.create_default_themes()


