"""
Module name: translator

This module configures the translator.
"""

import i18n

from game.utils.tools import resource_dir

translator = i18n
locales = {
    'en': 'English',
    'fr': 'Français',
    'ru': 'Русский',
    'pl': 'Polski'
    }

translator.set('filename_format', '{locale}.{format}')
translator.set('load_path', [resource_dir('game/assets/locales')])


def get_locale_from_language(language: str):
    """
    Return the locale (e.g.: 'en') of its associated language (e.g.: 'English').
    """
    return list(locales.keys())[list(locales.values()).index(language)]
