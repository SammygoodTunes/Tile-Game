
import socket
from threading import Thread

from game.utils.logger import logger
from game.network.protocol import Protocol
from game.network.packet import Hasher, Compressor


class Connection:
    """
    Class for creating a server connection.
    """

    PENDING, GETDATA = range(-1, -3, -1)
    SUCCESS, INVALID, REFUSED, TIMEOUT, NOROUTE = range(0, 5)

    def __init__(self, host: str, port: int):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(5.0)
        self.host = host
        self.port = port
        self.state = None
        logger.debug(f'Created {__class__.__name__} with attributes {self.__dict__}')

    def connect(self):
        try:
            self.state = Connection.PENDING
            self.sock.connect((socket.gethostbyname(socket.gethostname()) if self.host.lower() == 'localhost' else self.host, self.port))
            self.sock.send(Hasher.enhash(Protocol.RECOGNITION_CMD_REQ))
            data = self.sock.recv(Protocol.BUFFER_SIZE).decode(Protocol.ENCODING)
            if data and data == Hasher.hash(Protocol.RECOGNITION_CMD_RES):
                self.sock.send(Hasher.enhash(Protocol.MAPDATA_CMD_REQ))
            data = self.sock.recv(Protocol.BUFFER_SIZE).decode(Protocol.ENCODING)
            if data and data == Hasher.hash(Protocol.MAPDATA_CMD_RES):
                self.state = Connection.GETDATA
                compressed_map_data = b''
                data = self.sock.recv(Protocol.BUFFER_SIZE)
                while data != Hasher.enhash(Protocol.MAPREADY_CMD):
                    compressed_map_data += data
                    data = self.sock.recv(Protocol.BUFFER_SIZE)
                map_data = Compressor.decompress(compressed_map_data.strip())
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

    def start(self):
        connection_thread = Thread(target=self.connect)
        connection_thread.start()

