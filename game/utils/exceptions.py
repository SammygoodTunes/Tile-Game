

class InvalidTextureAtlas(Exception):

    def __init_(self, message="Invalid texture atlas, have you loaded one with set_atlas()?"):
        super().__init__(message)


class InvalidMapData(Exception):

    def __init(self, message="Invalid map data, have you initialise the map with initialise()?"):
        super().__init__(message)


class OutOfMapBounds(Exception):

    def __init__(self, message="Out of map boundaries, make sure to stay within them!"):
        super().__init__(message)
