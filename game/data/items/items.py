"""
Module name: items

This module defines the different game items.
"""

from game.data.items.item import Item
from game.utils.translator import translator as t


class Items:
	"""
	Class for creating a collection of items.
	"""

	AIR: Item = Item()
	SHOVEL: Item = Item(x=1, tooltip_name='Shovel').set_strength(16)
	GUN: Item = Item(x=2, tooltip_name='Gun')

	@staticmethod
	def translate():
		"""
		Translate the item tooltips.
		"""
		Items.SHOVEL.set_tooltip_name(t.t('data.items.shovel_name'))
		Items.GUN.set_tooltip_name(t.t('data.items.gun_name'))
