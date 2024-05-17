
import socket
from threading import Thread
from time import sleep

from game.client.player_manager import PlayerManager
from game.data.states import ConnectionStates
from game.entity.player import Player
from game.utils.logger import logger
from game.network import builders
from game.network.protocol import Protocol
from game.network.packet import Hasher, Compressor


class Tasks:
    """
    Class for defining the connection tasks.
    """

    CONNECT, UPDATE = range(0, 2)


class Connection:
    """
    Class for creating a server connection.
    """

    def __init__(self, host: str, port: int):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(30.0)
        self.sock.setblocking(True)
        self.host = host
        self.port = port
        self.state = ConnectionStates.IDLE
        self.player_manager = PlayerManager()
        self.player: Player | None = None
        self.data: any = None
        logger.debug(f'Created {__class__.__name__} with attributes {self.__dict__}')

    def connect(self) -> None:
        """
        Attempt to connect to a server with the provided host and port.
        Any errors or failures will raise specific exceptions.
        """
        try:
            self.state = ConnectionStates.PENDING
            self.sock.connect((socket.gethostbyname(socket.gethostname()) if self.host.lower() == 'localhost' else self.host, self.port))
            self.sock.send(Hasher.enhash(Protocol.RECOGNITION_CMD_REQ))
            self.sock.send(Hasher.enhash(Protocol.RECOGNITION_CMD_REQ))
            data = self.sock.recv(Protocol.BUFFER_SIZE).decode(Protocol.ENCODING)
            if data and data == Hasher.hash(Protocol.RECOGNITION_CMD_RES):
                self.sock.send(Hasher.enhash(Protocol.MAPOBJ_CMD_REQ))
            data = self.sock.recv(Protocol.BUFFER_SIZE).decode(Protocol.ENCODING)
            if data and data == Hasher.hash(Protocol.MAPOBJ_CMD_RES):
                self.state = ConnectionStates.GETDATA
                compressed_map_obj = b''
                data = self.sock.recv(Protocol.BUFFER_SIZE)
                while data != Hasher.enhash(Protocol.MAPREADY_CMD):
                    compressed_map_obj += data
                    data = self.sock.recv(Protocol.BUFFER_SIZE)
                self.data = Compressor.decompress(compressed_map_obj.strip())
                self.sock.send(Hasher.enhash(Protocol.PLAYERADD_CMD_REQ))
                player = builders.build_player(self.player)
                compressed_player_obj = Compressor.compress(player)
                self.sock.send(compressed_player_obj + b' ' * (Protocol.BUFFER_SIZE - len(compressed_player_obj) % Protocol.BUFFER_SIZE))
                self.sock.send(Hasher.enhash(Protocol.PLAYERADDREADY_CMD))
                self.state = ConnectionStates.SUCCESS
                return
            self.state = ConnectionStates.REFUSED
        except ConnectionRefusedError:
            self.state = ConnectionStates.REFUSED
        except TimeoutError:
            self.state = ConnectionStates.TIMEOUT
        except socket.gaierror:
            self.state = ConnectionStates.INVALID
        except OSError:
            self.state = ConnectionStates.NOROUTE
        except Exception:
            self.state = ConnectionStates.ERROR

    def disconnect(self) -> None:
        """
        Attempt to disconnect from the server.
        Any errors or failures will raise specific exceptions.
        """
        if self.state == ConnectionStates.SUCCESS:
            self.sock.send(Hasher.enhash(Protocol.DISCONNECT_CMD))
            self.state = ConnectionStates.IDLE
            #self.sock.close()

    def update(self):
        """
        Update and verify the connection every so often.
        """
        while self.state <= 0 and self.state != ConnectionStates.IDLE:
            try:
                data = self.sock.recv(Protocol.BUFFER_SIZE)
                if data and data == Hasher.enhash(Protocol.PLAYERUPDATE_CMD_RES):
                    compressed_player_obj = Compressor.compress(builders.build_player(self.player))
                    self.sock.send(compressed_player_obj + b' ' * (
                            Protocol.BUFFER_SIZE - len(compressed_player_obj) % Protocol.BUFFER_SIZE))
                    self.sock.send(Hasher.enhash(Protocol.PLAYERUPDATEREADY_CMD_RES))

                self.sock.send(Hasher.enhash(Protocol.PLAYERSUPDATE_CMD_REQ))
                self.sock.send(Hasher.enhash(Protocol.PLAYERUPDATE_CMD_REQ))
                data = self.sock.recv(Protocol.BUFFER_SIZE)
                if data and data == Hasher.enhash(Protocol.PLAYERSUPDATE_CMD_RES):
                    compressed_players_obj = b''
                    data = self.sock.recv(Protocol.BUFFER_SIZE)
                    while data != Hasher.enhash(Protocol.PLAYERSUPDATEREADY_CMD_RES):
                        compressed_players_obj += data
                        data = self.sock.recv(Protocol.BUFFER_SIZE)
                    players = Compressor.decompress(compressed_players_obj.strip())
                    self.player_manager.set_players(players)
            except BrokenPipeError:
                self.state = ConnectionStates.DISCONNECTED
            except OSError:
                self.state = ConnectionStates.DISCONNECTED

    def start(self, task: Tasks):
        connection_thread: Thread = Thread()
        if task == Tasks.CONNECT:
            connection_thread = Thread(target=self.connect)
        elif task == Tasks.UPDATE:
            connection_thread = Thread(target=self.update)
        connection_thread.start()
