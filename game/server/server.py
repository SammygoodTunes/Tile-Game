"""
Module name: server

This module handles the server and updates its state.
It also calls the server tasks that send data packets to the client.

(See data/states/server_states for the different server states.)
(See server/tasks for the different server tasks.)
"""

from multiprocessing import Process, Value
from threading import Thread
from time import sleep, time
import pygame.time
import socket

from game.data.properties.server_properties import ServerProperties
from game.data.states.server_states import ServerStates
from game.network.protocol import Protocol
from game.server.handlers.player_handler import PlayerHandler
from game.server.handlers.world_handler import WorldHandler
from game.server.tasks import ServerTasks
from game.utils.logger import logger


class Server:
    """
    Class for creating a new Server.
    """

    def __init__(self) -> None:
        self.state = Value('i', ServerStates.IDLE)
        self.player_count = Value('i', 0)
        self.sock: socket.socket | None = None
        self.server_thread: Process | None = None
        self.timer = Value('f', 0.0)
        self.world_handler: WorldHandler | None = None
        self.player_handler: PlayerHandler | None = None

    def client_handler(self, conn, addr) -> None:
        """
        Handle incoming server clients.
        """
        player_name: str = str()
        try:
            running = ServerTasks.recognition(conn, addr)
            ServerTasks.map_data(conn, addr, self.world_handler)
            player_name = ServerTasks.player_join(conn, self.player_handler)
            data = conn.recv(Protocol.BUFFER_SIZE)
            ServerTasks.game_state(conn, data, self.player_handler, self.world_handler)
            ServerTasks.local_game_state(conn)
            data = conn.recv(Protocol.BUFFER_SIZE)
            ServerTasks.incoming_packets(conn, data, self.player_handler, self.world_handler)
        except OSError:
            running = False

        logger.info(f'Connection from: {addr}')
        self.player_count.value = len(self.player_handler.get_players())
        while running:
            try:
                start_tile = time()
                if self.state.value == ServerStates.IDLE:
                    running = False
                    continue
                data = conn.recv(Protocol.BUFFER_SIZE)

                running = not ServerTasks.disconnection(data)
                if ServerTasks.game_state(conn, data, self.player_handler, self.world_handler):
                    ServerTasks.local_game_state(conn)
                ServerTasks.incoming_packets(conn, data, self.player_handler, self.world_handler)

                wait = time() - start_tile
                if not wait < 1 / ServerProperties.TICKS_PER_SECOND:
                    continue
                sleep(1 / ServerProperties.TICKS_PER_SECOND - wait)
            except ConnectionResetError:
                running = False
            except BrokenPipeError:
                running = False
            except OSError:
                running = False
        logger.info(f'Connection {addr} closing')
        self.timer.value = pygame.time.get_ticks() / 1000.0
        self.player_handler.untrack_player(player_name)
        self.player_count.value = len(self.player_handler.get_players())
        conn.close()

    def run(self, state, _seed: str, theme: dict, size: str) -> None:
        """
        Run the server and listen for connections.
        """
        self.world_handler = WorldHandler()
        self.player_handler = PlayerHandler()

        # Only IPv4 support for now
        # TODO: Add support for IPv6

        self.sock.listen()
        self.world_handler.create_world(_seed, theme, size)

        state.value = ServerStates.RUNNING

        while state.value == ServerStates.RUNNING:
            conn, addr = self.sock.accept()
            thread = Thread(target=self.client_handler, args=(conn, addr))
            thread.start()

    def start(self, _seed: str, theme: dict, size: str) -> None:
        """
        Prepare the server.
        """
        self.state.value = ServerStates.STARTING
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        host = '0.0.0.0'
        port = 35000

        try:
            self.sock.bind((host, port))
        except OSError as e:
            self.state.value = ServerStates.FAIL
            logger.error(f'Server failed to start: {e}')
            return
        logger.info(f'Starting server on {host}')
        self.server_thread = Process(target=self.run, args=(self.state, _seed, theme, size))
        self.server_thread.start()

    def stop(self) -> None:
        """
        Stop the server if it's running, otherwise don't do anything.
        """
        if self.state.value > 0:
            if self.server_thread is not None:
                self.server_thread.kill()
            self.sock.close()
            self.state.value = ServerStates.IDLE
            self.timer.value = 0.0
            logger.info('Server closed.')
            self.sock = None
            self.world_handler = None
            self.player_handler = None

    def safe_closure(self) -> None:
        """
        Safely close the server when no players are online after a certain amount of time.
        """
        if not self.state.value > 1 or not self.timer.value:
            return
        if (
                self.player_count.value <= 0
                and pygame.time.get_ticks() / 1000.0 - self.timer.value > ServerProperties.DELAY_BEFORE_CLOSURE
        ):
            logger.info(f'Closing server due to inactivity ({round(ServerProperties.DELAY_BEFORE_CLOSURE)}s delay)')
            self.stop()
