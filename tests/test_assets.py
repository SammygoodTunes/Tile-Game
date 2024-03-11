"""
Tests dedicated to the assets.
"""

from importlib import resources as impr
from os.path import isfile

from game import assets

ASSETS_DIR = impr.files(assets)


def test_assets_folder_exists():
    """
    Test: assets_folder_exists
    Desc: Tests if the asset folder exists.
    """
    assert ASSETS_DIR.is_dir()


def test_atlas_asset_exists():
    """
    Test: atlas_asset_exists
    Desc: Tests if the atlas asset exists in the asset directory.
    """
    assert isfile(ASSETS_DIR / 'atlas.png')


def test_font_asset_exists():
    """
    Test: font_asset_exists
    Desc: Tests if the font asset exists in the asset directory.
    """
    assert isfile(ASSETS_DIR / 'font.ttf')


def test_items_asset_exists():
    """
    Test: items_asset_exists
    Desc: Tests if the items asset exists in the asset directory.
    """
    assert isfile(ASSETS_DIR / 'items.png')


def test_player_asset_exist():
    """
    Test: player_asset_exists
    Desc: Tests if the player asset exists in the asset directory.
    """
    assert isfile(ASSETS_DIR / 'player.png')
