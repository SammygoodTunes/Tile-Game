
'''
Tests dedicated to the assets.
'''

from os.path import isfile
from importlib import resources as impr
from game import assets

ASSETS_DIR = impr.files(assets) 

def test_assets_folder_exists():
    assert ASSETS_DIR.is_dir()

def test_atlas_asset_exists():
    assert isfile(ASSETS_DIR / 'atlas.png')

def test_font_asset_exists():
    assert isfile(ASSETS_DIR / 'font.ttf')

def test_items_asset_exists():
    assert isfile(ASSETS_DIR / 'items.png')

def test_player_asset_exist():
    assert isfile(ASSETS_DIR / 'player.png')
