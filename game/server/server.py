
from threading import Thread
from multiprocessing import Process, Value
import socket
from time import sleep

from game.data.properties import ServerProperties
from game.data.states import ServerStates
from game.network.protocol import Protocol
from game.server.entity.player.player_handler import PlayerHandler
from game.server.tasks import Tasks
from game.server.world_handler import WorldHandler
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
            running = Tasks.recognition(conn, addr)
            Tasks.map_data(conn, addr, self.world_handler)
            player_name = Tasks.player_join(conn, self.player_handler)
            data = conn.recv(Protocol.BUFFER_SIZE)
            Tasks.game_state(conn, self.player_handler, data)
        except OSError:
            running = False
        print(f'Connection from: {addr}')
        self.player_count += 1
        while running:
            try:
                if self.state.value == ServerStates.IDLE:
                    running = False
                    continue
                data = conn.recv(Protocol.BUFFER_SIZE)
                # print(f'Message from {addr}: {data}')
                running = not Tasks.disconnection(data)
                # Tasks.player_hit(conn, self.player_handler, data)
                Tasks.incoming_packets(conn, self.player_handler, data)
                #Tasks.game_state(conn, self.player_handler, data)
                sleep(1.0 / ServerProperties.TICKS_PER_SECOND)
            except ConnectionResetError:
                running = False
            except BrokenPipeError:
                running = False
            except OSError:
                running = False
        print(f'Connection {addr} closing')
        self.player_handler.untrack_player(player_name)
        self.player_count -= 1
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
        print(f'Starting server on {host}')
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
