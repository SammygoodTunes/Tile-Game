
class Screen:
    """
    Class for creating a screen.
    """

    def __init__(self) -> None:
        self._enabled = False

    def set_state(self, state: bool) -> None:
        """
        Set the screen's visibility/interactivity.
        """
        self._enabled = state

    def get_state(self) -> bool:
        """
        Return the screen's visibility/interactivity state.
        """
        return self._enabled
