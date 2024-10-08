from math import ceil

from game.network.packet import Hasher, Compressor, fill, to_bytes, hex_len, Packet
from game.network.protocol import Protocol
from game.utils.exceptions import PlayerNameAlreadyExists, MaxPlayersReached


class ClientTasks:
    """
    Class for regrouping all client-side requests.
    """

    @staticmethod
    def recognition(sock) -> bool:
        """
        Task for client authenticity.
        Return True if the client's connection was successful, otherwise False.
        """
        sock.send(Hasher.enhash(Protocol.RECOGNITION_REQ))
        data = sock.recv(Protocol.BUFFER_SIZE)
        return data and data == Hasher.enhash(Protocol.RECOGNITION_RES)

    @staticmethod
    def map_data(sock) -> bool:
        """
        Task for requesting the map data.
        Return True if the map data response from the server was received successfully, otherwise False.
        """
        sock.send(Hasher.enhash(Protocol.MAPDATA_REQ))
        data = sock.recv(Protocol.BUFFER_SIZE)
        return data and data == Hasher.enhash(Protocol.MAPDATA_RES)

    @staticmethod
    def get_map_data(sock) -> bytes:
        """
        Task for receiving the map data object and decompressing it.
        Return the decompressed map data object once received.
        """
        compressed_map_obj = b''
        data = sock.recv(Protocol.BUFFER_SIZE)
        while data != Hasher.enhash(Protocol.MAPDATA_EOS):
            compressed_map_obj += data
            data = sock.recv(Protocol.BUFFER_SIZE)
        return Compressor.decompress(compressed_map_obj.strip())

    @staticmethod
    def player_join(sock) -> bool:
        """
        Task for joining a player to the server.
        Return True if the response from the server is received, otherwise False.
        """
        sock.send(Hasher.enhash(Protocol.PLAYERJOIN_REQ))
        data = sock.recv(Protocol.BUFFER_SIZE)
        return data and data == Hasher.enhash(Protocol.PLAYERJOIN_RES)

    @staticmethod
    def send_player_name(sock, player_name) -> bool:
        """
        Task for sending the client's name to the server.
        Raise exception when player name is already taken.
        """
        sock.send(player_name.encode(Protocol.ENCODING))
        data = sock.recv(Protocol.BUFFER_SIZE)
        if data == Hasher.enhash(Protocol.NAMEALREXIST_ERR):
            raise PlayerNameAlreadyExists
        if data == Hasher.enhash(Protocol.MAXPLAYERS_ERR):
            raise MaxPlayersReached
        return data and data == Hasher.enhash(Protocol.PLAYEROBJ_RES)

    @staticmethod
    def send_local_player(sock, player_manager) -> bool:
        """
        Task for sending the local player to the server.
        Return True if the local player packet was sent to and received by the server, otherwise False.
        """
        data = sock.recv(Protocol.BUFFER_SIZE)
        if not data or data != Hasher.enhash(Protocol.LCGAME_REQ):
            return False
        packet = player_manager.packetise_player()
        sock.send(fill(to_bytes(Protocol.PACKET_MAGIC) + hex_len(Compressor.compress(packet)) + Compressor.compress(packet)))
        data = sock.recv(Protocol.BUFFER_SIZE)
        return data and data == Hasher.enhash(Protocol.PACKETRECV_RES)

    @staticmethod
    def get_global_game_state(sock) -> list | None:
        """
        Task for receiving the global server-side game state.
        Return the game state list object if received successfully, otherwise None.
        """
        data = sock.recv(Protocol.BUFFER_SIZE)
        if not data or data != Hasher.enhash(Protocol.GLGAME_RES):
            return None

        compressed_players_obj = b''
        data = sock.recv(Protocol.BUFFER_SIZE)
        length = int(data[:Packet.DATA_SIZE], 16) + Packet.DATA_SIZE + 1
        data = data[Packet.DATA_SIZE:]
        for i in range(ceil(length / Protocol.BUFFER_SIZE)):
            if i != 0:
                data = sock.recv(Protocol.BUFFER_SIZE)
            compressed_players_obj += data
        return Compressor.decompress(compressed_players_obj.strip())
