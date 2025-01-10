"""
Module name: conf

Configuration for the documentation (readthedocs).
"""
import os
import sys

sys.path.insert(0, os.path.abspath('..'))

project = 'Tile-Game'
author = 'SammygoodTunes'
copyright = '%Y, SammygoodTunes'

version = '0.0.2a'
release = '0.0.2a'

language = 'en'

extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}

pygments_style = 'sphinx'

todo_include_todos = True

autodoc_default_options = {
    'members': True,
    'inherited-members': True,
    'show-inheritance': True,
}

autodoc_mock_imports = ['pygame', 'i18n', 'pyyaml']

htmlhelp_basename = 'tilegamedocs'

source_suffix = '.rst'
