"""
Module name: theme

This module allows for creating world themes.
"""

from typing import Self

from game.data.tiles.tile import Tile


class Theme:
    """
    Class for creating a world theme object.
    """

    def __init__(self, name: str = 'Untitled Theme'):
        self._name: str = name
        self._layers: list[dict[str, str | int]] | list = []

    def get_dict(self) -> dict[str, str | dict[str, str | int]]:
        """
        Return the theme as a dictionary.
        """
        return {
            'name': self._name,
            'layers': self._layers
        }

    def add_layer(self, layer_type: str, min_height: int, max_height: int, tile: Tile) -> Self:
        """
        Add a theme layer, then return the theme itself.
        """
        self._layers.append({
            'type': layer_type,
            'tile': tile.id,
            'min_height': min_height,
            'max_height': max_height,
        })
        return self

    def clear_layers(self) -> Self:
        """
        Clear all theme layers, then return the theme itself.
        """
        self._layers = ()
        return self

    def set_name(self, name: str) -> Self:
        """
        Set the theme name, then return the theme itself.
        """
        self._name = name
        return self

    def get_name(self) -> str:
        """
        Return the theme name.
        """
        return self._name

    def set_layers(self, layers: list[list[dict[str, str | int]]]) -> Self:
        """
        Set the theme layers, then return the theme itself.
        """
        self._layers = layers
        return self

    def get_layers(self) -> list[list[dict[str, str | int]]] | list:
        """
        Return the theme layers.
        """
        return self._layers
