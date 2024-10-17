"""
Module name: item_types

This module defines the item types. Need I say more?
"""

from game.data.items.items import Items


class ItemTypes:
	"""
	Class for regrouping items into different categories.
	"""

	TOOLS: tuple[Items] = (Items.SHOVEL,)
	WEAPONS: tuple[Items] = (Items.GUN,)
