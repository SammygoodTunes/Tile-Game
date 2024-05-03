
from game.client.connection import Connection
from game.gui.screens.serverjoin_screen import ServerJoinScreen
from game.gui.screens.serverconnect_screen import ServerConnectScreen


class ConnectionHandler:
    """
    Class for creating the connection handler.
    """

    def __init__(self):
        self.start_connection = False
        self.connection: Connection | None = None

    def update(self, join_screen: ServerJoinScreen, connection_screen: ServerConnectScreen):
        if self.start_connection:
            self.start_connection = False
            self.connection = Connection(join_screen.ip_input.get_text(), int(join_screen.port_input.get_text()))
            self.connection.start()

        if self.connection:
            connection_state = self.connection.state
            connection_screen.update_info_label(connection_state)
            if connection_state >= 0:
                self.connection = None

