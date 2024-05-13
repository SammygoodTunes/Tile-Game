
from threading import Thread
import socket
from time import time

from game.network.protocol import Protocol
from game.network.packet import Hasher, Compressor
from game.server.world_handler import WorldHandler

# logger = logging.getLogger(__name__)


class Server:
    """
    Class for creating a new Server.
    """

    IDLE, RUNNING = range(0, 2)

    def __init__(self):
        self.state = Server.IDLE
        self.player_count = 0
        self.sock: socket.socket | None = None
        self.timeout = 0
        self.world_handler: WorldHandler | None = None

    def client_handler(self, conn, addr):
        """
        Handle incoming server clients.
        """
        data = conn.recv(Protocol.BUFFER_SIZE).decode(Protocol.ENCODING)
        if data != Hasher.hash(Protocol.RECOGNITION_CMD_REQ):
            conn.close()
            return
        self.sock.settimeout(None)
        print(f'Connection from: {addr}')
        self.player_count += 1
        running = True
        while running:
            if self.state == Server.IDLE:
                running = False
                continue
            data = conn.recv(Protocol.BUFFER_SIZE).decode(Protocol.ENCODING)
            if data:
                print(f'Message from {addr}: {data}')
                if data == Hasher.hash(Protocol.DISCONNECT_CMD):
                    running = False
                elif data == Hasher.hash(Protocol.RECOGNITION_CMD_REQ):
                    print(f'Sending recognition message to {addr}')
                    conn.send(Hasher.enhash(Protocol.RECOGNITION_CMD_RES))
                elif data == Hasher.hash(Protocol.MAPOBJ_CMD_REQ):
                    print(f'Sending map to {addr}')
                    compressed_map_obj = Compressor.compress(self.world_handler.get_world().get_map())
                    conn.send(Hasher.enhash(Protocol.MAPOBJ_CMD_RES))
                    conn.send(compressed_map_obj + b' ' * (Protocol.BUFFER_SIZE - len(compressed_map_obj) % Protocol.BUFFER_SIZE))
                    conn.send(Hasher.enhash(Protocol.MAPREADY_CMD))
                    print(f'Sent!')
        print(f'Connection {addr} closing')
        self.player_count -= 1
        conn.close()

    def update(self):
        pass

    def run(self):
        """
        Run the server.
        """
        self.state = Server.RUNNING
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.world_handler = WorldHandler()

        '''logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(threadName)s] [%(levelname)s] - %(message)s',
            handlers=[
                logging.FileHandler(path.join(get_game_property(LOG_DIR), strftime('%d-%m-%Y-%H-%M-%S.log'))),
                logging.StreamHandler(sys.stdout)
            ]
        )'''

        # Only IPv4 support for now
        # TODO: Add support for IPv6

        host = socket.gethostbyname(socket.gethostname())
        port = 35000

        self.sock.bind((host, port))
        print(f'Started server on {host}')
        self.sock.listen()
        self.world_handler.create_world()

        while self.state == Server.RUNNING:
            conn, addr = self.sock.accept()
            thread = Thread(target=self.client_handler, args=(conn, addr))
            thread.start()

    def start(self):
        self.timeout = time()
        server_thread = Thread(target=self.run)
        server_thread.start()

    def stop(self):
        if self.state == Server.RUNNING:
            self.sock.close()
            self.state = Server.IDLE
            self.test()
            print(f'Server closed.')
            self.world_handler = None

    @staticmethod
    def test():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((socket.gethostbyname(socket.gethostname()), 35000))
            sock.send(Hasher.enhash('TEST'))
        except Exception:
            pass
