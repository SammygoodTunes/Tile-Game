
from game.data.items.items import Items
from game.data.properties.world_properties import WorldProperties


class DataTranslate:
    """
    Class for translating all data constants.
    """

    @staticmethod
    def translate_data():
        """
        Call all data translate methods to update data constants.
        """
        Items.translate()
        WorldProperties.translate()
