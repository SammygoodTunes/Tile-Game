
from game.client.connection import Connection, Tasks
from game.data.states import ConnectionStates


class ConnectionHandler:
    """
    Class for creating the connection handler.
    """

    def __init__(self):
        self.start_connection = False
        self.stop_connection = False
        self.host = None
        self.port = None
        self.connection: Connection | None = None

    def update(self, game):
        if self.start_connection:
            self.start_connection = False
            self.connection = Connection(
                game.screens.server_join_screen.ip_input.get_text() if self.host is None else self.host,
                int(game.screens.server_join_screen.port_input.get_text()) if self.port is None else self.port)
            game.player.set_player_name(game.screens.server_join_screen.ign_input.get_text().strip())
            self.connection.player = game.player
            self.connection.start(task=Tasks.CONNECT)

        if self.stop_connection:
            print('Disconnecting from server.')
            self.stop_connection = False
            self.connection.disconnect()
            self.connection = None

        if not self.connection:
            return

        connection_state = self.connection.state
        if not game.start_game:
            game.screens.server_connect_screen.update_info_label(connection_state)
            if connection_state > 0:
                self.connection = None
            if connection_state == ConnectionStates.SUCCESS:
                game.world.set_map(self.connection.data)
                game.world.initialise()
                game.world.get_map().load()
                game.player.set_ideal_spawn_point(game.world.get_map(), game.camera)
                game.start_game = True
                game.screens.server_connect_screen.set_state(False)
                self.connection.start(task=Tasks.UPDATE)

        if connection_state > 0 and game.start_game:
            game.start_game = False
            game.screens.server_connect_screen.set_state(True)

    def draw_other_players(self, game):
        self.connection.player_manager.draw_players(game.player.get_player_name(), game)
