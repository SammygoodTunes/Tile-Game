from game.network.packet import Hasher, Compressor
from game.network.protocol import Protocol


class Requests:
    """
    Class for regrouping all server-side requests.
    """

    @staticmethod
    def disconnection(data: bytes) -> bool:
        return data and data == Hasher.enhash(Protocol.DISCONNECT_CMD)

    @staticmethod
    def recognition(conn, addr, data: bytes) -> None:
        if data and data == Hasher.enhash(Protocol.RECOGNITION_CMD_REQ):
            print(f'Sending recognition message to {addr}')
            conn.send(Hasher.enhash(Protocol.RECOGNITION_CMD_RES))

    @staticmethod
    def map_data(conn, addr, world_handler, data: bytes) -> None:
        if data and data == Hasher.enhash(Protocol.MAPOBJ_CMD_REQ):
            print(f'Sending map to {addr}')
            compressed_map_obj = Compressor.compress(world_handler.get_world().get_map())
            conn.send(Hasher.enhash(Protocol.MAPOBJ_CMD_RES))
            conn.send(
                compressed_map_obj + b' ' * (Protocol.BUFFER_SIZE - len(compressed_map_obj) % Protocol.BUFFER_SIZE))
            conn.send(Hasher.enhash(Protocol.MAPREADY_CMD))
            print(f'Sent!')

    @staticmethod
    def player_tracking(conn, player_handler, data: bytes) -> None:
        if data and data == Hasher.enhash(Protocol.PLAYERADD_CMD_REQ):
            conn.send(Hasher.enhash(Protocol.PLAYERADD_CMD_RES))
            compressed_player_obj = b''
            data = conn.recv(Protocol.BUFFER_SIZE)
            while data != Hasher.enhash(Protocol.PLAYERADDREADY_CMD):
                compressed_player_obj += data
                data = conn.recv(Protocol.BUFFER_SIZE)
            player_handler.track_player(Compressor.decompress(compressed_player_obj.strip()))

    @staticmethod
    def player_data(conn, player_handler, data: bytes) -> None:
        if data and data == Hasher.enhash(Protocol.PLAYERSUPDATE_CMD_REQ):
            compressed_players_obj = Compressor.compress(player_handler.get_players())
            conn.send(Hasher.enhash(Protocol.PLAYERSUPDATE_CMD_RES))
            conn.send(compressed_players_obj + b' ' * (Protocol.BUFFER_SIZE - len(compressed_players_obj) % Protocol.BUFFER_SIZE))
            conn.send(Hasher.enhash(Protocol.PLAYERSUPDATEREADY_CMD_RES))

    @staticmethod
    def player_update(conn, player_handler, data: bytes) -> None:
        if data and data == Hasher.enhash(Protocol.PLAYERUPDATE_CMD_REQ):
            conn.send(Hasher.enhash(Protocol.PLAYERUPDATE_CMD_RES))
            compressed_player_obj = b''
            data: bytes = conn.recv(Protocol.BUFFER_SIZE)
            while data != Hasher.enhash(Protocol.PLAYERUPDATEREADY_CMD_RES):
                if not data.isalnum():
                    compressed_player_obj += data
                data = conn.recv(Protocol.BUFFER_SIZE)
            player = Compressor.decompress(compressed_player_obj.strip())
            player_handler.update_player(player)
