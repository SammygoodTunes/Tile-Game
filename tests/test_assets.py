
from os.path import exists, isfile, join

ASSETS_DIR = 'assets'

def test_assets_folder_exists():
	assert exists(ASSETS_DIR)

def test_atlas_asset_exists():
	assert exists(join(ASSETS_DIR, 'atlas.png'))

def test_font_asset_exists():
	assert exists(join(ASSETS_DIR, 'font.ttf'))

def test_items_asset_exists():
	assert exists(join(ASSETS_DIR, 'items.png'))

def test_player_asset_exist():
	assert exists(join(ASSETS_DIR, 'player.png'))