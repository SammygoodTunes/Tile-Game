"""
Module name: server_states

This module defines the different states of the server.
"""

class ServerStates:
    """
    Server states.
    """

    IDLE, STARTING, RUNNING, FAIL = range(0, 4)
