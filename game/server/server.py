
from threading import Thread
import socket

from data.protocol import Protocol

# logger = logging.getLogger(__name__)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def client(conn, addr):
    print(f'Connection from: {addr}')
    running = True
    while running:
        data = conn.recv(Protocol.BUFFER_SIZE).decode(Protocol.ENCODING)
        if data:
            print(f'Message from {addr}: {data}')
            if data == Protocol.DISCONNECT_CMD.encode(Protocol.ENCODING):
                running = False
    print(f'Connection {addr} closing')
    conn.close()


def server():
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
    try:
        host = socket.gethostbyname(socket.gethostname())
        port = 35000

        sock.bind((host, port))
        print(f'Started server on {host}')
        sock.listen()
        while running:
            conn, addr = sock.accept()
            thread = Thread(target=client, args=(conn, addr))
            thread.start()
    except Exception as e:
        print(e)
