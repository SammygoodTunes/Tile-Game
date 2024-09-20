
from math import ceil
from pygame.event import Event
import socket
from threading import Thread
from time import sleep
import traceback

from game.client.player_manager import PlayerManager
from game.client.tasks import ClientTasks
from game.data.properties import ServerProperties
from game.data.states import ConnectionStates
from game.utils.exceptions import PlayerWithSameNameError
from game.utils.logger import logger
from game.network.protocol import Protocol
from game.network.packet import Hasher, Compressor, fill, to_bytes, hex_len, Packet


class Tasks:
    """
    Class for defining the connection tasks.
    """

    CONNECT, UPDATE = range(0, 2)


class Connection:
    """
    Class for creating a server connection.
    """

    def __init__(self, host: str, port: int, client) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(30.0)
        self.sock.setblocking(True)
        self.host = host
        self.port = port
        self.state = ConnectionStates.IDLE
        self.packet_queue: list[dict] = list()  # FIFO
        self.player_manager = PlayerManager(client.player)
        self.data: any = None
        self.hit_player = str()
        logger.debug(f'Created {__class__.__name__} with attributes {self.__dict__}')

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
            self.data = ClientTasks.get_map_data(self.sock)

            if not ClientTasks.player_join(self.sock):
                self.state = ConnectionStates.REFUSED
                return

            if not ClientTasks.send_player_name(self.sock, player_name):
                self.state = ConnectionStates.REFUSED
                return

            self.player_manager.local_player.set_player_name(player_name)

            if not ClientTasks.send_local_player(self.sock, self.player_manager):
                self.state = ConnectionStates.REFUSED
                return

            self.sock.send(Hasher.enhash(Protocol.GLGAME_REQ))
            self.player_manager.set_players(ClientTasks.get_global_game_state(self.sock))

            if self.player_manager.get_player(player_name=player_name) is None:
                self.state = ConnectionStates.REFUSED
                raise PlayerWithSameNameError
            self.state = ConnectionStates.SUCCESS
        except PlayerWithSameNameError:
            self.state = ConnectionStates.BADNAME
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
        if self.state == ConnectionStates.SUCCESS:
            try:
                print('Disconnecting from server.')
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
        success: bool = True

        while self.state <= 0 and self.state != ConnectionStates.IDLE:
            try:
                if success:
                    self.sock.send(Hasher.enhash(Protocol.GLGAME_REQ))
                players = ClientTasks.get_global_game_state(self.sock)
                self.player_manager.set_players(players)
                success = players is not None
                if success:
                    ClientTasks.send_local_player(self.sock, self.player_manager)

                '''elif data and data == Hasher.enhash(Protocol.HIT_RES):
                    print('Client: received hit response, sending hit player name============================')
                    self.sock.send(fill(self.hit_player.encode(Protocol.ENCODING)))'''
                sleep(1 / ServerProperties.TICKS_PER_SECOND)
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
