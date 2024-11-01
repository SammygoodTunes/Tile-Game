"""
Module name: theme_manager

This module manages the world generation theme, as well as generating the default themes JSON file.
"""

from os import path
from game.utils.translator import translator as tr
import json

from game.data.themes.themes import Themes
from game.utils.logger import logger


class ThemeManager:
    """
    Class for creating the theme manager.
    """

    THEMES_FILE = 'themes.json'

    @staticmethod
    def init_themes() -> None:
        """
        Initialise the world themes.
        """
        Themes.DEFAULT.set_name('world.themes.default')
        Themes.HELL.set_name('world.themes.hell')
        Themes.ISLANDS.set_name('world.themes.islands')
        Themes.HELL_ISLANDS.set_name('world.themes.hell_islands')

    @staticmethod
    def create_default_themes() -> None:
        """
        Create the default world themes files.
        """
        ThemeManager.init_themes()
        json_data = json.dumps({
            'themes': [
                Themes.DEFAULT.get_dict(),
                Themes.HELL.get_dict(),
                Themes.ISLANDS.get_dict(),
                Themes.HELL_ISLANDS.get_dict()
            ]
        }, indent=4)
        with open(ThemeManager.THEMES_FILE, 'w') as theme_file:
            theme_file.write(json_data)

    @staticmethod
    def check_themes() -> None:
        """
        Check the themes directory and its files.
        """
        if not path.isfile(ThemeManager.THEMES_FILE):
            logger.info('Creating themes file as none were found.')
            ThemeManager.create_default_themes()

    @staticmethod
    def get_theme_by_id(theme_id: int) -> dict:
        """
        Return the theme dict from the themes file by theme name.
        """
        themes = ThemeManager.get_themes()['themes']
        for i, theme in enumerate(themes):
            if theme['id'] == theme_id:
                return theme
        return {}

    @staticmethod
    def get_themes() -> dict:
        """
        Retrieve and return the themes JSON data from the themes file as a dict object.
        """
        ThemeManager.check_themes()
        with open(ThemeManager.THEMES_FILE) as theme_file:
            json_data = theme_file.read()
        return json.loads(json_data)

    @staticmethod
    def get_theme_names() -> list:
        """
        Retrieve and return the different theme names that exist as a list.
        """
        ThemeManager.check_themes()
        with open(ThemeManager.THEMES_FILE) as theme_file:
            themes_dict = json.loads(theme_file.read())
        return [tr.t(themes_dict['themes'][i]['name']) for i, _ in enumerate(themes_dict['themes'])]
