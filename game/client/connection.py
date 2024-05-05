
import socket
from threading import Thread
from time import time, sleep

from game.utils.logger import logger
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

    IDLE, PENDING, GETDATA = range(-1, -4, -1)
    SUCCESS, INVALID, REFUSED, TIMEOUT, NOROUTE, DISCONNECTED, ERROR = range(0, 7)

    def __init__(self, host: str, port: int):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(5.0)
        self.host = host
        self.port = port
        self.state = Connection.IDLE
        self.data: any = None
        logger.debug(f'Created {__class__.__name__} with attributes {self.__dict__}')

    def connect(self) -> None:
        """
        Attempt to connect to a server with the provided host and port.
        Any errors or failures will raise specific exceptions.
        """
        try:
            self.state = Connection.PENDING
            self.sock.connect((socket.gethostbyname(socket.gethostname()) if self.host.lower() == 'localhost' else self.host, self.port))
            self.sock.send(Hasher.enhash(Protocol.RECOGNITION_CMD_REQ))
            data = self.sock.recv(Protocol.BUFFER_SIZE).decode(Protocol.ENCODING)
            if data and data == Hasher.hash(Protocol.RECOGNITION_CMD_RES):
                self.sock.send(Hasher.enhash(Protocol.MAPOBJ_CMD_REQ))
            data = self.sock.recv(Protocol.BUFFER_SIZE).decode(Protocol.ENCODING)
            if data and data == Hasher.hash(Protocol.MAPOBJ_CMD_RES):
                self.state = Connection.GETDATA
                compressed_map_obj = b''
                data = self.sock.recv(Protocol.BUFFER_SIZE)
                while data != Hasher.enhash(Protocol.MAPREADY_CMD):
                    compressed_map_obj += data
                    data = self.sock.recv(Protocol.BUFFER_SIZE)
                self.data = Compressor.decompress(compressed_map_obj.strip())
                self.state = Connection.SUCCESS
                return
            self.state = Connection.REFUSED
        except ConnectionRefusedError:
            self.state = Connection.REFUSED
        except TimeoutError:
            self.state = Connection.TIMEOUT
        except socket.gaierror:
            self.state = Connection.INVALID
        except OSError:
            self.state = Connection.NOROUTE
        except Exception:
            self.state = Connection.ERROR

    def disconnect(self) -> None:
        """
        Attempt to disconnect from the server.
        Any errors or failures will raise specific exceptions.
        """
        if self.state == Connection.SUCCESS:
            self.sock.send(Hasher.enhash(Protocol.DISCONNECT_CMD))
            self.state = Connection.IDLE
            self.sock.close()

    def update(self):
        """
        Update and verify the connection every so often.
        """
        while self.state <= 0 and self.state != Connection.IDLE:
            try:
                self.sock.send(Hasher.enhash(Protocol.VERIFY_CMD))
                sleep(5)
            except BrokenPipeError:
                self.state = Connection.DISCONNECTED

    def start(self, task: Tasks):
        connection_thread: Thread = Thread()
        if task == Tasks.CONNECT:
            connection_thread = Thread(target=self.connect)
        elif task == Tasks.UPDATE:
            connection_thread = Thread(target=self.update)
        connection_thread.start()
