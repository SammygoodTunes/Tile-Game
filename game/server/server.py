
from os import path, mkdir
from threading import Thread
from time import strftime
import logging
import socket
import sys

from data.data_manager import get_game_property, SERVER_VER, HOST, LOG_DIR, PORT
from data.protocol import Protocol

logger = logging.getLogger(__name__)
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

    if not path.exists(get_game_property(LOG_DIR)):
        mkdir(get_game_property(LOG_DIR), 0o755)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(threadName)s] [%(levelname)s] - %(message)s',
        handlers=[
            logging.FileHandler(path.join(get_game_property(LOG_DIR), strftime('%d-%m-%Y-%H-%M-%S.log'))),
            logging.StreamHandler(sys.stdout)
        ]
    )

    logger.info(f'Starting server (v{get_game_property(SERVER_VER)})...')

    # Only IPv4 support for now
    # TODO: Add support for IPv6
    try:
        host = get_game_property(HOST)
        port = int(get_game_property(PORT))

        if not host:
            host = socket.gethostbyname(socket.gethostname())

        sock.bind((host, port))
        print(f'Started server on {host}')
        sock.listen()
        logger.info(f'Server listening on port {port}')
        while running:
            conn, addr = sock.accept()
            thread = Thread(target=client, args=(conn, addr))
            thread.start()
    except Exception as e:
        print(e)
