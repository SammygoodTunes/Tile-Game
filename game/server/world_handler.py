
from game.world.world import World


class WorldHandler:
    """
    Class for a creating the world handler.
    """

    def __init__(self):
        self._world: World = World()

    def create_world(self):
        """
        Create a new server world.
        """
        self._world.create()

    def get_world(self):
        """
        Return the world object.
        """
        return self._world
