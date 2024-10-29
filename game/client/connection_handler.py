"""
Module name: connection_handler

This module acts as a pathway between the client and connection modules.
This means that whatever the connection module doesn't have access to, the connection handler will provide it with
what it needs. This is because most of the connection handling done by the connection module is run on a different
thread. And the way the modules are structure disallow for any direct communication between the client and connection
modules.
Shared attributes probably will (eventually) be implemented to make it thread-safe(r).
"""

from pygame.event import Event
from time import time

from game.client.connection import Connection, Tasks
from game.data.states.connection_states import ConnectionStates
from game.world.world import World


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

    def events(self, e: Event) -> None:
        """
        Handle the connection handler events.
        """
        if not self.connection:
            return
        self.connection.events(e)

    def update(self, game) -> None:
        """
        Keep track of the connection state.
        """

        if self.start_connection:
            self.start_connection = False
            game.client.world = World(64, 64)
            game.client.world.initialise()
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

        if self.connection.world_manager.temp_data:
            game.client.world.get_map().update(self.connection.world_manager.temp_data)

        if not game.start_game:
            game.screens.server_connect_screen.update_info_label(connection_state)
            if connection_state > 0:
                self.connection = None
            if connection_state == ConnectionStates.SUCCESS:
                game.client.world.initialise()
                game.client.world.get_map().load()
                game.client.player.set_ideal_spawn_point(game.client.world.get_map(), game.client.camera)
                game.paused = False
                game.start_game = True
                game.screens.server_connect_screen.set_state(False)
                self.connection.start(task=Tasks.UPDATE)

        if connection_state > 0 and game.start_game:
            game.start_game = False
            self.stop_connection = True
            game.screens.server_connect_screen.update_info_label(self.connection.state)
            game.screens.pause_screen.set_state(False)
            game.screens.options_screen.set_state(False)
            game.screens.server_connect_screen.set_state(True)

    def draw_other_players(self, game, delta) -> None:
        """
        Display all other server players.
        We don't draw the main player as it is redundant.
        """
        self.connection.player_manager.draw_players(game.client.player.get_player_name(), delta, game)

    def queue_packet(self, packet: bytes) -> None:
        """
        Queue a packet in the packet queue.
        """
        if not self.connection:
            print('Cannot queue packet as connection has not been started.')
            return
        self.connection.packet_queue.append(packet)

    def get_ping(self) -> int:
        """
        Return the connection ping, only if a connection has been established.
        """
        if not self.connection:
            return 0
        return self.connection.ping

    def get_total_data_sent(self) -> float:
        """
        Return the total data sent to the server, rounded to megabytes (not mebibytes).
        """
        if not self.connection:
            return 0.0
        return self.connection.sock.get_sent() / 1_000_000.0

    def get_total_data_received(self) -> float:
        """
        Return the total data received from the server, rounded to megabytes (not mebibytes).
        """
        if not self.connection:
            return 0.0
        return self.connection.sock.get_recv() / 1_000_000.0

    def get_average_data_sent(self) -> float:
        """
        Return the average data sent per minute, rounded to kilobytes (not kibibytes).
        """
        if not self.connection:
            return 0.0
        if self.connection.timer is None:
            return 0.0
        return self.connection.sock.get_sent() / (time() - self.connection.timer) * 60 / 1000.0

    def get_average_data_received(self) -> float:
        """
        Return the average data received per minute, rounded to kilobytes (not kibibytes).
        """
        if not self.connection:
            return 0.0
        if self.connection.timer is None:
            return 0.0
        return self.connection.sock.get_recv() / (time() - self.connection.timer) * 60 / 1000.0

    def get_players(self) -> list:
        """
        Return the current players in the server, otherwise return an empty list if no connection has been established.
        """
        if not self.connection:
            return list()
        return self.connection.player_manager.players
