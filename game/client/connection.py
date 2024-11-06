"""
Module name: connection

This particular module handles the connection to a server, its state and all of its tasks.
It also calls the client tasks that send data packets to the server.

(See data/states/connection_states for the different connection states.)
(See client/tasks for the different client tasks.)
"""

from pygame.event import Event
from pygame.time import get_ticks
from threading import Thread
from time import time
import socket
import traceback

from game.client.managers.player_manager import PlayerManager
from game.client.managers.world_manager import WorldManager
from game.client.tasks import ClientTasks
from game.data.states.connection_states import ConnectionStates
from game.network.packet import Hasher
from game.network.protocol import Protocol
from game.utils.exceptions import PlayerNameAlreadyExists, MaxPlayersReached
from game.utils.logger import logger


class Tasks:
    """
    Class for defining the connection tasks.
    """

    CONNECT, UPDATE = range(0, 2)


class XSocket(socket.socket):
    """
    Class for socket with extra byte counter.
    """

    def __init__(self, family=socket.AF_INET, type_=socket.SOCK_STREAM, proto=0, fileno=None):
        super().__init__(family, type_, proto, fileno)
        self._sent: int = 0
        self._recv: int = 0
        self._s_tmp: int = 0  # Stores the total bytes sent (updated every second)
        self._r_tmp: int = 0  # Stores the total bytes received (updated every second)
        self.old_s_tmp = 0  # Stores the old temporary value of _s_tmp (updated every second)
        self.old_r_tmp = 0  # Stores the old temporary value of _r_tmp (updated every second)
        self.timer = get_ticks() / 1000.0

    def send(self, buffer: bytes, flags: int = 0) -> int:
        """
        Override socket send with counter.
        """
        bufsize = super().send(buffer, flags)
        self._sent += bufsize
        return bufsize

    def recv(self, bufsize: int, flags: int = 0) -> bytes:
        """
        Override socket recv with counter.
        """
        buffer = super().recv(bufsize, flags)
        self._recv += len(buffer)
        return buffer

    def get_sent(self) -> int:
        """
        Return total bytes sent to the server since the existence of the socket.
        """
        return self._sent

    def get_recv(self) -> int:
        """
        Return total bytes received from the server since the existence of the socket.
        """
        return self._recv

    def set_s_tmp(self) -> None:
        """
        Set temporary total bytes to current total bytes sent from the server since the existence of the socket.
        """
        self.old_s_tmp = self._s_tmp
        self._s_tmp = self._sent

    def set_r_tmp(self) -> None:
        """
        Set temporary total bytes to current total bytes received from the server since the existence of the socket.
        """
        self.old_r_tmp = self._r_tmp
        self._r_tmp = self._recv

    def get_s_tmp(self) -> int:
        """
        Return temporary total bytes sent from the server.
        """
        return self._s_tmp

    def get_r_tmp(self) -> int:
        """
        Return temporary total bytes received from the server.
        """
        return self._r_tmp


class Connection:
    """
    Class for creating a server connection.
    """

    def __init__(self, host: str, port: int, client) -> None:
        self.sock = XSocket()
        self.sock.settimeout(10.0)
        self.host = host
        self.port = port
        self.state = ConnectionStates.IDLE
        self.packet_queue: list[bytes] = []  # FIFO
        self.player_manager = PlayerManager(client.player)
        self.world_manager = WorldManager(client.world)
        self.ping: int = 0
        self.hit_player = str()
        self.timer: float | None = None

    def connect(self, player_name: str) -> None:
        """
        Attempt to connect to a server with the provided host and port.
        Any errors or failures will raise specific exceptions.
        """
        try:
            self.timer = get_ticks() / 1000.0
            self.state = ConnectionStates.PENDING
            self.sock.connect((socket.gethostbyname(socket.gethostname()) if self.host.lower() == 'localhost' else self.host, self.port))
            if not ClientTasks.recognition(self.sock):
                raise ConnectionRefusedError('Failed to recognise client.')

            ClientTasks.map_data(self.sock)
            data = self.sock.recv(Protocol.BUFFER_SIZE)
            if not ClientTasks.confirm_map_data(data):
                raise ConnectionRefusedError('Failed to get map data.')
            self.state = ConnectionStates.GETDATA
            self.world_manager.build_world_from_bytes(ClientTasks.get_map_data(self.sock), update_map_size=True)

            if not ClientTasks.player_join(self.sock):
                raise ConnectionRefusedError('Failed to join server.')

            if not ClientTasks.send_player_name(self.sock, player_name):
                raise ConnectionRefusedError('Failed to get player name.')

            self.player_manager.local_player.set_player_name(player_name)

            self.sock.send(Hasher.enhash(Protocol.GLGAME_REQ))
            data = self.sock.recv(Protocol.BUFFER_SIZE)
            game_state = ClientTasks.get_global_game_state(self.sock, data)
            if game_state is None or not game_state:
                raise ConnectionRefusedError('Failed to get global game state.')
            players = game_state[1:game_state[0] + 1]
            map_data = game_state[game_state[0] + 1:]
            self.player_manager.set_players(players)
            self.world_manager.build_dynatile_from_bytes(map_data)

            data = self.sock.recv(Protocol.BUFFER_SIZE)
            if not ClientTasks.send_local_player(self.sock, data, self.player_manager):
                raise ConnectionRefusedError('Failed to send local player.')

            data = self.sock.recv(Protocol.BUFFER_SIZE)
            if not ClientTasks.confirm_local_player(data):
                raise ConnectionRefusedError('Failed to confirm local player.')

            self.state = ConnectionStates.SUCCESS
        except PlayerNameAlreadyExists as e:
            logger.error(f'Connection aborted: {e}')
            self.state = ConnectionStates.BADNAME
            self.disconnect()
        except MaxPlayersReached as e:
            logger.error(f'Connection aborted: {e}')
            self.state = ConnectionStates.MAXIMUM
            self.disconnect()
        except ConnectionRefusedError as e:
            logger.error(f'Connection refused: {e}')
            self.state = ConnectionStates.REFUSED
            self.disconnect()
        except TimeoutError:
            logger.error(f'Connection timed out!')
            self.state = ConnectionStates.TIMEOUT
            self.disconnect()
        except socket.gaierror:
            logger.error(f'Unknown host')
            self.state = ConnectionStates.INVALID
            self.disconnect()
        except OSError as e:
            logger.error(f'Internal error: {e}')
            self.state = ConnectionStates.NOROUTE
            self.disconnect()
        except Exception as e:
            logger.debug(f'Exception: {e}')
            logger.error(f'{traceback.format_exc()}')
            self.state = ConnectionStates.ERROR
            self.disconnect()

    def disconnect(self) -> None:
        """
        Attempt to disconnect from the server.
        Any errors or failures will raise specific exceptions.
        """
        if not self.state in [
            ConnectionStates.SUCCESS,
            ConnectionStates.TIMEOUT
        ]:
            return
        try:
            logger.info('Disconnecting from server.')
            self.sock.send(Hasher.enhash(Protocol.DISCONNECT_REQ))
            self.packet_queue.clear()
            self.timer = None
        except (ConnectionResetError, BrokenPipeError):
            pass
        self.state = ConnectionStates.IDLE

    def events(self, e: Event) -> None:
        """
        Handle the connection events (unused).
        """
        pass

    def update(self) -> None:
        """
        Update and verify the connection every so often.
        """
        _local_player_sent: bool = False
        _queued_packet_sent: bool = False
        _players_received: bool = False
        _map_data_sent: bool = False

        _game_state: bytes = b''

        packet_recv_timestamp = time()
        self.sock.send(Hasher.enhash(Protocol.GLGAME_REQ))

        while self.state <= 0 and self.state != ConnectionStates.IDLE:
            try:

                data = self.sock.recv(Protocol.BUFFER_SIZE)

                _game_state = ClientTasks.get_global_game_state(self.sock, data)

                if _local_player_sent:
                    ClientTasks.confirm_local_player(data)
                    self.sock.send(Hasher.enhash(Protocol.GLGAME_REQ))
                    self.ping = round((time() - packet_recv_timestamp) * 1000)
                    packet_recv_timestamp = time()

                if _queued_packet_sent:
                    ClientTasks.confirm_queued_packet(data)
                    self.ping = round((time() - packet_recv_timestamp) * 1000)
                    packet_recv_timestamp = time()

                _local_player_sent = ClientTasks.send_local_player(self.sock, data, self.player_manager)
                _queued_packet_sent = ClientTasks.check_packet_queue(self.sock, self.packet_queue)

                if _game_state:
                    players = _game_state[1:_game_state[0] + 1]
                    map_data = _game_state[_game_state[0] + 1:]
                    self.player_manager.set_players(players)
                    self.world_manager.build_dynatile_from_bytes(map_data)
                    self.ping = round((time() - packet_recv_timestamp) * 1000)
                    packet_recv_timestamp = time()

                if get_ticks() / 1000.0 - self.sock.timer >= 1:
                    self.sock.set_s_tmp()
                    self.sock.set_r_tmp()
                    self.sock.timer = get_ticks() / 1000.0

            except TimeoutError:
                self.state = ConnectionStates.TIMEOUT
            except BrokenPipeError:
                self.state = ConnectionStates.DISCONNECTED
            except OSError:
                self.state = ConnectionStates.DISCONNECTED

    def start(self, task: Tasks, player_name: str = "") -> None:
        """
        Start a client connection task.
        """
        connection_thread: Thread = Thread()
        if task == Tasks.CONNECT:
            connection_thread = Thread(target=self.connect, args=(player_name,))
        elif task == Tasks.UPDATE:
            connection_thread = Thread(target=self.update)
        connection_thread.start()
