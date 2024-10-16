from math import ceil

from game.client.managers.player_manager import PlayerManager
from game.network.builders.player_builder import PlayerBuilder
from game.network.builders.base_builder import BaseBuilder
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
    def map_data(sock) -> None:
        """
        Task for requesting the map data.
        Return True if the map data response from the server was received successfully, otherwise False.
        """
        sock.send(Hasher.enhash(Protocol.MAPDATA_REQ))

    @staticmethod
    def confirm_map_data(data: bytes) -> bool:
        """
        Task for confirming the reception of the map data request.
        Returns True if the data is a valid server response, otherwise False.
        """
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
    def send_local_player(sock, data: bytes, player_manager: PlayerManager) -> bool:
        """
        Task for sending the local player to the server.
        Return True if the local player packet was sent to and received by the server, otherwise False.
        """
        if not data or data != Hasher.enhash(Protocol.LCGAME_REQ):
            return False
        packet = PlayerBuilder.get_compressed_player_packet(
            BaseBuilder.PLAYER_POSITION_UPDATE_COMMAND,
            player_manager.local_player
        )
        sock.send(fill(to_bytes(Protocol.SPACKET_MAGIC) + hex_len(packet) + packet))
        return True

    @staticmethod
    def confirm_local_player(data: bytes) -> bool:
        """
        Task for confirming the reception of the local player sent to the server.
        Return True if the data is a valid packet reception response, otherwise False.
        """
        return data and data == Hasher.enhash(Protocol.PACKETRECV_RES)

    @staticmethod
    def get_global_game_state(sock, data: bytes) -> bytes | None:
        """
        Task for receiving the global server-side game state.
        Return the game state list object if received successfully, otherwise None.
        """
        if not data or data != Hasher.enhash(Protocol.GLGAME_RES):
            return None
        compressed_game_state = b''
        data = sock.recv(Protocol.BUFFER_SIZE)
        length = int.from_bytes(data[:Packet.DATA_SIZE])
        n_packets = ceil(length / Protocol.BUFFER_SIZE)
        data = data[Packet.DATA_SIZE:Packet.DATA_SIZE + length]
        if n_packets == 1:
            return data
        for i in range(n_packets):
            if i != 0: data = sock.recv(Protocol.BUFFER_SIZE)[:length - i * Protocol.BUFFER_SIZE]
            compressed_game_state += data
        return compressed_game_state

    @staticmethod
    def check_packet_queue(sock, queue: list[bytes]) -> bool:
        """
        Task for verifying the packet queue.
        If a packet is present, take the first one, send it to the server and remove it from the queue.
        [FIFO]
        """
        if not queue:
            return False
        sock.send(fill(to_bytes(Protocol.SPACKET_MAGIC) + hex_len(queue[0]) + queue[0]))
        queue.pop(0)
        return True

    @staticmethod
    def confirm_queued_packet(data) -> bool:
        """
        Task for confirming the reception of the queued packet that was sent to the server.
        Return True if the data is a valid packet reception response, otherwise False.
        """
        return data and data == Hasher.enhash(Protocol.PACKETRECV_RES)