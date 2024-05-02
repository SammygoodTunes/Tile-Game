
import socket
from threading import Thread

from game.utils.logger import logger


class Connection:
    """
    Class for creating a server connection.
    """

    PENDING, SUCCESS, INVALID, REFUSED, TIMEOUT, NOROUTE = range(0, 6)

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
            print(self.host, socket.gethostbyname(socket.gethostname()))
            self.sock.connect((socket.gethostbyname(socket.gethostname()) if self.host.lower() == 'localhost' else self.host, self.port))
            self.state = Connection.SUCCESS
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

