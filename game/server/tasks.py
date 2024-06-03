from game.network.packet import Hasher, Compressor
from game.network.protocol import Protocol


class Tasks:
    """
    Class for regrouping all server-side requests.
    """

    @staticmethod
    def disconnection(data: bytes) -> bool:
        """
        Task for disconnecting a player.
        """
        return data and data == Hasher.enhash(Protocol.DISCONNECT_REQ)

    @staticmethod
    def recognition(conn, addr) -> bool:
        """
        Task for checking for player authenticity.
        """
        data = conn.recv(Protocol.BUFFER_SIZE)
        if data and data == Hasher.enhash(Protocol.RECOGNITION_REQ):
            print(f'Sending recognition message to {addr}')
            conn.send(Hasher.enhash(Protocol.RECOGNITION_RES))
            return True
        return False

    @staticmethod
    def map_data(conn, addr, world_handler) -> None:
        """
        Task for sending map data to a client.
        """
        data = conn.recv(Protocol.BUFFER_SIZE)
        if data and data == Hasher.enhash(Protocol.MAPDATA_REQ):
            print(f'Sending map to {addr}')
            compressed_map_obj = Compressor.compress(world_handler.get_world().get_map())
            conn.send(Hasher.enhash(Protocol.MAPDATA_RES))
            conn.send(
                compressed_map_obj + b' ' * (Protocol.BUFFER_SIZE - len(compressed_map_obj) % Protocol.BUFFER_SIZE))
            conn.send(Hasher.enhash(Protocol.MAPDATA_READY_RES))
            print(f'Sent!')

    @staticmethod
    def send_game_state(conn, player_handler) -> None:
        """
        Task for sending the overall game state to a client.
        """
        conn.send(Hasher.enhash(Protocol.GAMEUPDATE_RES))
        compressed_players_obj = Compressor.compress(player_handler.get_players())
        conn.send(compressed_players_obj + b' ' * (Protocol.BUFFER_SIZE - len(compressed_players_obj) % Protocol.BUFFER_SIZE))
        conn.send(Hasher.enhash(Protocol.GAMEUPDATE_READY_RES))

    @staticmethod
    def player_update(conn, player_handler, data: bytes) -> str:
        """
        Task for receiving a client's player data.
        """
        if data and data == Hasher.enhash(Protocol.PLAYERUPDATE_REQ):
            print("Got player request, sending response")
            conn.send(Hasher.enhash(Protocol.PLAYERUPDATE_RES))
            compressed_player_obj = b''
            data: bytes = conn.recv(Protocol.BUFFER_SIZE)
            while data != Hasher.enhash(Protocol.PLAYERUPDATE_READY_RES):
                print(b'Waiting for ready response: '+Hasher.enhash(Protocol.PLAYERUPDATE_READY_RES))
                compressed_player_obj += data
                data = conn.recv(Protocol.BUFFER_SIZE)
            print('Got ready response, decompressing')
            print(compressed_player_obj)
            player = Compressor.decompress(compressed_player_obj.strip())
            if player is None:
                print("player is none, returning empty string")
                return str()
            player_handler.update_player(player)
            return player['name']
        return str()
