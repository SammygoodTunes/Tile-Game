"""
Module name: items

This module defines the different game items.
"""

from game.data.items.item import Item


class Items:
	"""
	Class for creating a collection of items.
	"""

	AIR: Item = Item()
	SHOVEL: Item = Item(x=1, tooltip_name="Shovel").set_strength(16)
	GUN: Item = Item(x=2, tooltip_name="Gun")
