"""
Module name: translator

This module configures the translator.
"""

import i18n

from game.utils.tools import resource_dir

translator = i18n

# Disable languages that are not complete and correct for certain.
locales = {
    'en': 'English',
    'fr': 'Français',
    # 'es': 'Español',
    # 'ru': 'Русский',
    # 'pl': 'Polski',
    # 'zh': '简体中文',
    # 'jp': '日本語',
    }

translator.set('filename_format', '{locale}.{format}')
translator.set('load_path', [resource_dir('game/assets/locales')])


def get_locale_from_language(language: str) -> str:
    """
    Return the locale (e.g.: 'en') of its associated language (i.e.: 'English').
    """
    return list(locales.keys())[list(locales.values()).index(language)]
