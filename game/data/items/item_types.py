from game.data.items.items import Items


class ItemTypes:
	"""
	Class for regrouping items into different categories.
	"""

	TOOLS: tuple[Items] = (Items.SHOVEL,)
	WEAPONS: tuple[Items] = (Items.GUN,)
