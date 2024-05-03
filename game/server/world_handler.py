
from game.world.world import World


class WorldHandler:
    """
    Class for a creating the world handler.
    """

    def __init__(self):
        self.world: World = World()

    def create_world(self):
        """
        Create a new server world.
        """
        self.world.initialise()

    def get_map_data(self):
        """
        Return the map data of the world.
        """
        return self.world.get_map().get_data()
