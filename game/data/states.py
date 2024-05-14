
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