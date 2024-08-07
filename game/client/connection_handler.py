
from pygame.event import Event

from game.client.connection import Connection, Tasks
from game.data.states import ConnectionStates


class ConnectionHandler:
    """
    Class for creating the connection handler.
    """

    def __init__(self) -> None:
        self.start_connection = False
        self.stop_connection = False
        self.host = None
        self.port = None
        self.player_name = None
        self.connection: Connection | None = None

    def events(self, e: Event):
        if not self.connection:
            return
        self.connection.events(e)

    def update(self, game) -> None:
        """
        Keep track of the connection state.
        """
        if self.start_connection:
            self.start_connection = False
            self.connection = Connection(
                game.screens.server_join_screen.ip_input.get_text() if self.host is None else self.host,
                int(game.screens.server_join_screen.port_input.get_text()) if self.port is None else self.port,
                game.client
            )
            self.connection.start(task=Tasks.CONNECT, player_name=self.player_name)

        if self.stop_connection:
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
                game.client.world.set_map(self.connection.data)
                game.client.world.initialise()
                game.client.world.get_map().load()
                game.client.player.set_ideal_spawn_point(game.client.world.get_map(), game.client.camera)
                game.paused = False
                game.start_game = True
                game.screens.server_connect_screen.set_state(False)
                self.connection.start(task=Tasks.UPDATE)

        if connection_state > 0 and game.start_game:
            game.start_game = False
            game.screens.pause_screen.set_state(False)
            game.screens.server_connect_screen.set_state(True)

    def update_ui(self, game):
        if not self.connection:
            return
        self.connection.player_manager.player.update_ui(game)

    def draw_other_players(self, game, delta) -> None:
        """
        Display all other server players.
        We don't draw the main player as it is redundant.
        """
        self.connection.player_manager.draw_players(game.client.player.get_player_name(), delta, game)

    def queue_packet(self, packet: dict) -> None:
        if not self.connection:
            print('Cannot queue packet as connection has not been started.')
            return
        self.connection.packet_queue.append(packet)
        print(f'[{len(self.connection.packet_queue)}] Queued packet: {packet}')

