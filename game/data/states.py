
class MapStates:
    """
    Map states.
    """
    GENMAP = 'GEN-MAP'
    READY = 'READY'


class ConnectionStates:
    """
    Connection states.
    """
    IDLE, PENDING, GETDATA = range(-1, -4, -1)
    SUCCESS, INVALID, REFUSED, TIMEOUT, NOROUTE, DISCONNECTED, ERROR = range(0, 7)


class ServerStates:
    """
    Server states.
    """
    IDLE, STARTING, RUNNING = range(0, 3)


class MouseStates:
    """
    Mouse states.
    """

    LMB, MMB, RMB, SCROLL_UP, SCROLL_DOWN = range(1, 6)


class PlayerStates:
    """
    Player states.
    """

    MOVE_DOWN, MOVE_RIGHT, MOVE_UP, MOVE_LEFT = range(3, -1, -1)
