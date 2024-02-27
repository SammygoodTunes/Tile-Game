
from enum import Enum

class Item:

	def __init__(self, tooltip_name, x, y):
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
	SHOVEL = Item("Shovel", 0, 0).set_strength(2.5).set_durability(200)

class ItemTypes(Enum):
	TOOLS = [Items.SHOVEL]
