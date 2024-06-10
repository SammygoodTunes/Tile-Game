import pygame
from pygame.event import Event
import socket
from threading import Thread
from time import sleep
import traceback

from game.client.player_manager import PlayerManager
from game.data.properties import ServerProperties
from game.data.states import ConnectionStates, MouseStates
from game.entity.player import Player
from game.utils.exceptions import PlayerWithSameNameError
from game.utils.logger import logger
from game.network import builders
from game.network.protocol import Protocol
from game.network.packet import Hasher, Compressor, fill


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
        self.player_manager = PlayerManager(client.player)
        self.player: Player | None = None
        self.data: any = None
        self.recv_player_update = True
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
            self.sock.send(Hasher.enhash(Protocol.RECOGNITION_REQ))
            data = self.sock.recv(Protocol.BUFFER_SIZE).decode(Protocol.ENCODING)
            if not data or data != Hasher.hash(Protocol.RECOGNITION_RES):
                self.state = ConnectionStates.REFUSED
                return
            self.sock.send(Hasher.enhash(Protocol.MAPDATA_REQ))
            data = self.sock.recv(Protocol.BUFFER_SIZE).decode(Protocol.ENCODING)
            if not data or data != Hasher.hash(Protocol.MAPDATA_RES):
                self.state = ConnectionStates.REFUSED
                return
            self.state = ConnectionStates.GETDATA
            compressed_map_obj = b''
            data = self.sock.recv(Protocol.BUFFER_SIZE)
            while data != Hasher.enhash(Protocol.MAPDATA_EOS):
                compressed_map_obj += data
                data = self.sock.recv(Protocol.BUFFER_SIZE)
            self.data = Compressor.decompress(compressed_map_obj.strip())

            self.sock.send(Hasher.enhash(Protocol.PLAYERJOIN_REQ))
            data = self.sock.recv(Protocol.BUFFER_SIZE)
            if not data or data != Hasher.enhash(Protocol.PLAYERJOIN_RES):
                self.state = ConnectionStates.REFUSED
                return
            self.sock.send(player_name.encode(Protocol.ENCODING))
            data = self.sock.recv(Protocol.BUFFER_SIZE)
            if not data and data != Hasher.enhash(Protocol.PLAYEROBJ_RES):
                self.state = ConnectionStates.REFUSED
                return
            compressed_player_obj = b''
            data = self.sock.recv(Protocol.BUFFER_SIZE)
            while data != Hasher.enhash(Protocol.PLAYEROBJ_EOS):
                compressed_player_obj += data
                data = self.sock.recv(Protocol.BUFFER_SIZE)
            player_obj = Compressor.decompress(compressed_player_obj)
            self.player_manager.build_local_player(player_obj)

            self.sock.send(Hasher.enhash(Protocol.GAMEUPDATE_REQ))
            data = self.sock.recv(Protocol.BUFFER_SIZE)
            if not data or data != Hasher.enhash(Protocol.GAMEUPDATE_RES):
                self.state = ConnectionStates.REFUSED
                return
            compressed_players_obj = b''
            data = self.sock.recv(Protocol.BUFFER_SIZE)
            while data != Hasher.enhash(Protocol.GAMEUPDATE_EOS):
                compressed_players_obj += data
                data = self.sock.recv(Protocol.BUFFER_SIZE)
            self.player_manager.set_players(Compressor.decompress(compressed_players_obj.strip()))
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
        while self.state <= 0 and self.state != ConnectionStates.IDLE:
            try:
                self.sock.send(Hasher.enhash(Protocol.GAMEUPDATE_REQ))
                print('Sent game update request')
                # make predictions about the game like player movement
                data = self.sock.recv(Protocol.BUFFER_SIZE)
                if data and data == Hasher.enhash(Protocol.GAMEUPDATE_RES):
                    print('Received game update response')
                    compressed_players_obj = b''
                    data = self.sock.recv(Protocol.BUFFER_SIZE)
                    while data != Hasher.enhash(Protocol.GAMEUPDATE_EOS):
                        compressed_players_obj += data
                        data = self.sock.recv(Protocol.BUFFER_SIZE)
                    players = Compressor.decompress(compressed_players_obj.strip())
                    print(players)
                    self.player_manager.set_players(players)
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
