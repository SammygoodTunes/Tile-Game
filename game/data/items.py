
from enum import Enum
from importlib import resources as impr
from game import assets


class Item:

	DEFAULT_ATLAS = impr.files(assets) / "items.png"

	def __init__(self, x=0, y=0, tooltip_name=""):
		self._xy = (x, y)
		self._tooltip_name = tooltip_name
		self._strength = 0
		self._durability = -1

	def set_xy(self, x, y):
		self._xy = (x, y)
		return self

	def get_xy(self):
		return self._xy

	def set_tooltip_name(self, tooltip_name):
		self._tooltip_name = tooltip_name
		return self

	def get_tooltip_name(self):
		return self._tooltip_name

	def set_strength(self, strength):
		self._strength = strength
		return self

	def get_strength(self):
		return self._strength

	def set_durability(self, durability):
		self._durability = durability
		return self

	def get_durability(self):
		return self._durability

class Items(Enum):
	AIR = Item()
	SHOVEL = Item(x=1, tooltip_name="Shovel").set_strength(10).set_durability(200)

class ItemTypes(Enum):
	TOOLS = [Items.SHOVEL]
