
from importlib import resources as impr
from typing import Self

from game.utils.logger import logger


class Item:
	"""
	Class for creating a usable item.
	"""

	DEFAULT_ATLAS: str = str(impr.files('assets') / "items.png")

	def __init__(self, x: int = 0, y: int = 0, tooltip_name: str = '') -> None:
		self._xy: tuple[int, int] = (x, y)
		self._tooltip_name: str = tooltip_name
		self._strength: int = 0
		self._durability: int = -1
		logger.debug(f'Created {__class__.__name__} with attributes {self.__dict__}')

	def __eq__(self, obj: Self):
		if not isinstance(obj, Item):
			return False
		return (
				self._xy == obj.get_xy()
				and self._tooltip_name == self.get_tooltip_name()
				and self._strength == self.get_strength()
				and self._durability == self.get_durability()
		)

	def set_xy(self, x: int, y: int) -> Self:
		"""
		Set the texture coordinates of the item, then return the item itself.
		"""
		self._xy = (x, y)
		return self

	def get_xy(self) -> tuple[int, int]:
		"""
		Return the texture coordinates of the item.
		"""
		return self._xy

	def set_tooltip_name(self, tooltip_name: str) -> Self:
		"""
		Set the tooltip name of the item, then return the item itself.
		"""
		self._tooltip_name = tooltip_name
		return self

	def get_tooltip_name(self) -> str:
		"""
		Return the tooltip name of the item.
		"""
		return self._tooltip_name

	def set_strength(self, strength: int) -> Self:
		"""
		Set the strength of the item, then return the item itself.
		"""
		self._strength = strength
		return self

	def get_strength(self) -> int:
		"""
		Return the strength of the item.
		"""
		return self._strength

	def set_durability(self, durability: int) -> Self:
		"""
		Set the durability of the item, then return the item itself.
		"""
		self._durability = durability
		return self

	def get_durability(self) -> int:
		"""
		Return the durability of the item.
		"""
		return self._durability


class Items:
	"""
	Class for creating a collection of items.
	"""

	AIR: Item = Item()
	SHOVEL: Item = Item(x=1, tooltip_name="Shovel").set_strength(10)
	GUN: Item = Item(x=2, tooltip_name="Gun").set_strength(5)


class ItemTypes:
	"""
	Class for regrouping items into different categories.
	"""

	TOOLS: tuple[Items] = (Items.SHOVEL,)
	WEAPONS: tuple[Items] = (Items.GUN,)
