
from threading import Thread
from multiprocessing import Process, Value
import socket
from time import sleep, time

from game.data.properties.server_properties import ServerProperties
from game.data.states.server_states import ServerStates
from game.network.protocol import Protocol
from game.server.handlers.player_handler import PlayerHandler
from game.server.tasks import ServerTasks
from game.server.handlers.world_handler import WorldHandler
from game.utils.logger import logger


class Server:
    """
    Class for creating a new Server.
    """

    def __init__(self) -> None:
        self.state = Value('i', ServerStates.IDLE)
        self.player_count = 0
        self.sock: socket.socket | None = None
        self.server_thread: Process | None = None
        self.timeout = 0
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
        self.player_count = len(self.player_handler.get_players())
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
        self.player_handler.untrack_player(player_name)
        self.player_count = len(self.player_handler.get_players())
        conn.close()

    def run(self, state, _seed: str) -> None:
        """
        Run the server and listen for connections.
        """
        self.world_handler = WorldHandler()
        self.player_handler = PlayerHandler()

        # Only IPv4 support for now
        # TODO: Add support for IPv6

        self.sock.listen()
        self.world_handler.create_world(_seed)

        state.value = ServerStates.RUNNING

        while state.value == ServerStates.RUNNING:
            conn, addr = self.sock.accept()
            thread = Thread(target=self.client_handler, args=(conn, addr))
            thread.start()

    def start(self, _seed: str) -> None:
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
        self.server_thread = Process(target=self.run, args=(self.state, _seed))
        self.server_thread.start()

    def stop(self) -> None:
        """
        Stop the server if it's running, otherwise don't do anything.
        """
        if self.state.value in (ServerStates.STARTING, ServerStates.RUNNING):
            if self.server_thread is not None:
                self.server_thread.kill()
            self.sock.close()
            self.state.value = ServerStates.IDLE
            logger.info('Server closed.')
            self.sock = None
            self.world_handler = None
            self.player_handler = None
