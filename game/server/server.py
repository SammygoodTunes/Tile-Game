
from threading import Thread
import socket

from game.network.protocol import Protocol
from game.network.packet import Hasher, Compressor
from game.server.world_handler import WorldHandler

# logger = logging.getLogger(__name__)


class Server:
    """
    Class for creating a new Server.
    """

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.world_handler: WorldHandler | None = None


    def client_handler(self, conn, addr):
        """
        Handle incoming server clients.
        """
        print(f'Connection from: {addr}')
        running = True
        while running:
            data = conn.recv(Protocol.BUFFER_SIZE).decode(Protocol.ENCODING)
            if data:
                print(f'Message from {addr}: {data}')
                if data == Hasher.hash(Protocol.DISCONNECT_CMD):
                    running = False
                elif data == Hasher.hash(Protocol.RECOGNITION_CMD_REQ):
                    print(f'Sending recognition message to {addr}')
                    conn.send(Hasher.enhash(Protocol.RECOGNITION_CMD_RES))
                elif data == Hasher.hash(Protocol.MAPDATA_CMD_REQ):
                    print(f'Sending map data to {addr}')
                    compressed_map_data = Compressor.compress(self.world_handler.get_map_data())
                    conn.send(Hasher.enhash(Protocol.MAPDATA_CMD_RES))
                    conn.send(compressed_map_data + b' ' * (Protocol.BUFFER_SIZE - len(compressed_map_data) % Protocol.BUFFER_SIZE))
                    conn.send(Hasher.enhash(Protocol.MAPREADY_CMD))
                    print(f'Sent!')
        print(f'Connection {addr} closing')
        conn.close()

    def run(self):
        """
        Run the server.
        """
        self.world_handler = WorldHandler()
        running = True

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
        data = Compressor.compress(self.world_handler.get_map_data())
        while running:
            conn, addr = self.sock.accept()
            thread = Thread(target=self.client_handler, args=(conn, addr))
            thread.start()


server = Server()
server.run()
