"""
Module name: translator

This module configures the translator.
"""

import i18n

from game.utils.tools import resource_dir

translator = i18n
locales = {'en': 'English', 'fr': 'Français'}

translator.set('filename_format', '{locale}.{format}')
translator.set('error_on_missing_translation', True)
translator.set('load_path', [resource_dir('game/assets/locales')])
