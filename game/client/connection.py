
from pygame.event import Event
import socket
from threading import Thread
from time import sleep, time
import traceback

from game.client.managers.player_manager import PlayerManager
from game.client.managers.world_manager import WorldManager
from game.client.tasks import ClientTasks
from game.data.properties.server_properties import ServerProperties
from game.data.states.connection_states import ConnectionStates
from game.utils.exceptions import PlayerNameAlreadyExists, MaxPlayersReached
from game.utils.logger import logger
from game.network.protocol import Protocol
from game.network.packet import Hasher


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
        Get total bytes sent to the server since the existence of the socket.
        """
        return self._sent

    def get_recv(self) -> int:
        """
        Get total bytes received from the server since the existence of the socket.
        """
        return self._recv


class Connection:
    """
    Class for creating a server connection.
    """

    def __init__(self, host: str, port: int, client) -> None:
        self.sock = XSocket()
        self.sock.settimeout(30.0)
        self.sock.setblocking(True)
        self.host = host
        self.port = port
        self.state = ConnectionStates.IDLE
        self.packet_queue: list[bytes] = list()  # FIFO
        self.player_manager = PlayerManager(client.player)
        self.world_manager = WorldManager(client.world)
        self.ping: int = 0
        self.total_data_sent: int = 0 # in bytes
        self.hit_player = str()


    def connect(self, player_name: str) -> None:
        """
        Attempt to connect to a server with the provided host and port.
        Any errors or failures will raise specific exceptions.
        """
        try:
            self.state = ConnectionStates.PENDING
            self.sock.connect((socket.gethostbyname(socket.gethostname()) if self.host.lower() == 'localhost' else self.host, self.port))
            if not ClientTasks.recognition(self.sock):
                self.state = ConnectionStates.REFUSED
                return
            if not ClientTasks.map_data(self.sock):
                self.state = ConnectionStates.REFUSED
                return
            self.state = ConnectionStates.GETDATA
            self.world_manager.build_world_from_bytes(ClientTasks.get_map_data(self.sock))

            if not ClientTasks.player_join(self.sock):
                self.state = ConnectionStates.REFUSED
                return

            if not ClientTasks.send_player_name(self.sock, player_name):
                self.state = ConnectionStates.REFUSED
                return

            self.player_manager.local_player.set_player_name(player_name)

            self.sock.send(Hasher.enhash(Protocol.GLGAME_REQ))
            data = self.sock.recv(Protocol.BUFFER_SIZE)
            game_state = ClientTasks.get_global_game_state(self.sock, data)
            players = game_state[1:game_state[0] + 1]
            map_state = game_state[game_state[0] + 1:][self.world_manager.queue_offset:]
            self.player_manager.set_players(players)
            if map_state:
                self.world_manager.update_broken_tiles(map_state)

            data = self.sock.recv(Protocol.BUFFER_SIZE)
            if not ClientTasks.send_local_player(self.sock, data, self.player_manager):
                self.state = ConnectionStates.REFUSED
                return

            data = self.sock.recv(Protocol.BUFFER_SIZE)
            if not ClientTasks.confirm_local_player(data):
                self.state = ConnectionStates.REFUSED
                return

            self.state = ConnectionStates.SUCCESS
        except PlayerNameAlreadyExists:
            self.state = ConnectionStates.BADNAME
        except MaxPlayersReached:
            self.state = ConnectionStates.MAXIMUM
        except ConnectionRefusedError:
            self.state = ConnectionStates.REFUSED
        except TimeoutError:
            self.state = ConnectionStates.TIMEOUT
        except socket.gaierror:
            self.state = ConnectionStates.INVALID
        except OSError:
            self.state = ConnectionStates.NOROUTE
        except Exception:
            logger.error(f'{traceback.format_exc()}')
            self.state = ConnectionStates.ERROR

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
        except (ConnectionResetError, BrokenPipeError):
            pass
        self.state = ConnectionStates.IDLE

    def events(self, e: Event) -> None:
        """
        if e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == MouseStates.LMB:
                hit_player = self.player_manager.hit_player(self.player.get_player_name())
                if not hit_player:
                    return
                print(f"Hit player {hit_player}, sending packets to server")
                self.hit_player = hit_player
        """
        pass

    def update(self) -> None:
        """
        Update and verify the connection every so often.
        """
        _local_player_sent: bool = False
        _queued_packet_sent: bool = False
        _players_received: bool = False
        self.sock.settimeout(10.0)
        self.sock.send(Hasher.enhash(Protocol.GLGAME_REQ))

        while self.state <= 0 and self.state != ConnectionStates.IDLE:
            try:
                data = self.sock.recv(Protocol.BUFFER_SIZE)
                packet_recv_timestamp = time()

                game_state = ClientTasks.get_global_game_state(self.sock, data)
                if game_state is not None:
                    self.ping = round((time() - packet_recv_timestamp) * 1000)
                    players = game_state[1:game_state[0] + 1]
                    self.player_manager.set_players(players)
                    _players_received = players is not None
                    map_state = game_state[game_state[0] + 1:][self.world_manager.queue_offset:]
                    if map_state: self.world_manager.update_broken_tiles(map_state)

                if _local_player_sent:
                    ClientTasks.confirm_local_player(data)
                    self.ping = round((time() - packet_recv_timestamp) * 1000)
                    self.sock.send(Hasher.enhash(Protocol.GLGAME_REQ))

                if _queued_packet_sent:
                    ClientTasks.confirm_queued_packet(data)
                    self.ping = round((time() - packet_recv_timestamp) * 1000)

                _local_player_sent = ClientTasks.send_local_player(self.sock, data, self.player_manager)
                _queued_packet_sent = ClientTasks.check_packet_queue(self.sock, self.packet_queue)

                wait = time() - packet_recv_timestamp
                if wait < 1 / ServerProperties.TICKS_PER_SECOND:
                    sleep(1 / ServerProperties.TICKS_PER_SECOND - wait)
            except TimeoutError:
                self.state = ConnectionStates.TIMEOUT
            except BrokenPipeError:
                self.state = ConnectionStates.DISCONNECTED
            except OSError:
                self.state = ConnectionStates.DISCONNECTED

    def start(self, task: Tasks, player_name: str = "") -> None:
        connection_thread: Thread = Thread()
        if task == Tasks.CONNECT:
            connection_thread = Thread(target=self.connect, args=(player_name,))
        elif task == Tasks.UPDATE:
            connection_thread = Thread(target=self.update)
        connection_thread.start()
