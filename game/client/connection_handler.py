
from pygame.event import Event

from game.client.connection import Connection, Tasks
from game.data.states import ConnectionStates
from game.data.structures import TileStructure
from game.gui.label import Label
from game.world.map_manager import Map


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
                width, height = self.connection.data[0], self.connection.data[1]
                tile_data_pos = width * height * TileStructure.TILE_BYTE_SIZE
                game.client.world.set_map(Map(width, height))
                game.client.world.get_map().set_tile_data(self.connection.data[2:tile_data_pos])
                game.client.world.get_map().set_dynatile_data(self.connection.data[tile_data_pos + 1:])
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

    def draw_other_players(self, game, delta) -> None:
        """
        Display all other server players.
        We don't draw the main player as it is redundant.
        """
        self.connection.player_manager.draw_players(game.client.player.get_player_name(), delta, game)

    def queue_packet(self, packet: dict) -> None:
        """
        Queue a packet in the packet queue.
        """
        if not self.connection:
            print('Cannot queue packet as connection has not been started.')
            return
        self.connection.packet_queue.append(packet)

    def get_ping(self) -> int:
        """
        Get the connection ping, only if a connection has been established.
        """
        if not self.connection:
            return 0
        return self.connection.ping

    def get_total_data_sent(self) -> float:
        """
        Get the total data sent to the server, rounded to megabytes (not mebibytes).
        """
        if not self.connection:
            return 0.0
        return self.connection.sock.get_sent() / 1_000_000.0

    def get_total_data_received(self) -> float:
        """
        Get the total data received from the server, rounded to megabytes (not mebibytes).
        """
        if not self.connection:
            return 0.0
        return self.connection.sock.get_recv() / 1_000_000.0

    def get_players(self) -> list:
        """
        Get the current players in the server, otherwise return an empty list if no connection has been established.
        """
        if not self.connection:
            return list()
        return self.connection.player_manager.players