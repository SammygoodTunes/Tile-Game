
class ConnectionStates:
    """
    Connection states.
    """
    IDLE, PENDING, GETDATA = range(-1, -4, -1)
    SUCCESS, INVALID, REFUSED, TIMEOUT, NOROUTE, DISCONNECTED, BADNAME, MAXIMUM, ERROR, SERVFAIL = range(0, 10)
