
project = 'Tile-Game'
author = 'SammygoodTunes'
copyright = '%Y, SammygoodTunes, Jaztylap, o.nihilist, Pickmonde'

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

htmlhelp_basename = 'tilegamedocs'

source_suffix = '.rst'
