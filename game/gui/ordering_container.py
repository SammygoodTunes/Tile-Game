"""
Module name: ordering_container
"""

from typing import Self

from pygame import KEYDOWN, K_TAB, KMOD_SHIFT
from pygame.event import Event

from game.gui.inputbox import InputBox
from game.gui.widget import Widget


class OrderingContainer(Widget):
    """
    Class for creating an ordering container.
    This is used for containing widgets that require ordering, like for tabbing between widgets.
    This isn't a visible GUI component.
    """

    def __init__(self) -> None:
        super().__init__(0, 0)
        self._order: int = -1
        self._widgets: list[any] = []

    def events(self, e: Event) -> None:
        if not self._enabled or not self._can_interact:
            return
        if e.type != KEYDOWN:
            return
        if e.key != K_TAB:
            return

        # Input boxes
        if not isinstance(self._widgets[self._order], InputBox) or not self._order >= -1:
            return
        for i, widget in enumerate(self._widgets):
            if widget.is_selected():
                self._order = i
                break
        [widget.set_selected(False) for widget in self._widgets]
        if e.mod & KMOD_SHIFT:
            self._order = self._order - 1 if self._order > 0 else len(self._widgets) - 1
        else:
            self._order = self._order + 1 if self._order < len(self._widgets) - 1 else 0
        self._widgets[self._order].set_selected(True)

    def set_widgets(self, widgets: list[any]) -> Self:
        """
        Set the ordering container's widgets array, then return the ordering container itself
        """
        self._widgets = widgets
        return self

    def get_widgets(self) -> list[any]:
        """
        Return the ordering container's widgets array.
        """
        return self._widgets

    def set_state(self, state: bool) -> Self:
        super().set_state(state)
        self._order = -1
        return self

    def set_interact(self, state: bool) -> Self:
        super().set_interact(state)
        for widget in self._widgets:
            widget.set_interact(state)
        return self

