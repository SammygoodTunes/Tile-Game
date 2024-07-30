from game.data.items import Items
from game.network.builders import PlayerBuilder, BaseBuilder
from game.network.packet import Hasher, Compressor, to_bytes
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
            conn.send(compressed_map_obj + b' ' * (Protocol.BUFFER_SIZE - len(compressed_map_obj) % Protocol.BUFFER_SIZE))
            conn.send(Hasher.enhash(Protocol.MAPDATA_EOS))
            print(f'Sent!')

    @staticmethod
    def player_join(conn, player_handler) -> str:
        """
        Task for joining a client player to the server.
        Returns the received player name.
        """
        player_name: str = str()
        data = conn.recv(Protocol.BUFFER_SIZE)
        if data and data == Hasher.enhash(Protocol.PLAYERJOIN_REQ):
            print('got player join request, sending response')
            conn.send(Hasher.enhash(Protocol.PLAYERJOIN_RES))
        data = conn.recv(Protocol.BUFFER_SIZE)
        if data:
            player_name = data.decode(Protocol.ENCODING)
            player_dict = PlayerBuilder.create_player()
            player_dict[PlayerBuilder.NAME_KEY] = player_name
            player_handler.update_player(player_dict)
            compressed_player = Compressor.compress(player_dict)
            conn.send(Hasher.enhash(Protocol.PLAYEROBJ_RES))
            conn.send(compressed_player + b' ' * (Protocol.BUFFER_SIZE - len(compressed_player) % Protocol.BUFFER_SIZE))
            conn.send(Hasher.enhash(Protocol.PLAYEROBJ_EOS))
        return player_name if player_name else str()

    @staticmethod
    def game_state(conn, player_handler, data: bytes) -> None:
        """
        Task for sending the overall game state to a client.
        """
        if not data or data != Hasher.enhash(Protocol.GAMEUPDATE_REQ):
            return
        conn.send(Hasher.enhash(Protocol.GAMEUPDATE_RES))
        compressed_players_obj = Compressor.compress(player_handler.get_players())
        conn.send(compressed_players_obj + b' ' * (Protocol.BUFFER_SIZE - len(compressed_players_obj) % Protocol.BUFFER_SIZE))
        conn.send(Hasher.enhash(Protocol.GAMEUPDATE_EOS))

    @staticmethod
    def incoming_packets(conn, player_handler, data: bytes) -> None:
        """
        Task for handling incoming packets
        """
        if not data or data[:len(Protocol.PACKET_MAGIC)] != to_bytes(Protocol.PACKET_MAGIC):
            return
        print('incoming packet')
        packet = b''
        data = data[len(Protocol.PACKET_MAGIC):]
        while data != Hasher.enhash(Protocol.PACKET_EOS):
            print(f'Got data: {data}')
            packet += data
            data = conn.recv(Protocol.BUFFER_SIZE)
        decompressed_packet = Compressor.decompress(packet)
        if not isinstance(decompressed_packet, dict):
            print('Packet received is not of instance \'dict\'')
            return
        print(decompressed_packet)
        type_id = decompressed_packet[BaseBuilder.COMMAND_ID_KEY]
        print(f'Received packet of type {type_id}.')
        if type_id == BaseBuilder.PLAYER_MOVE_COMMAND_ID:
            player_handler.move_player(decompressed_packet)

    @staticmethod
    def player_hit(conn, player_handler, data: bytes) -> None:
        if not data or data != Hasher.enhash(Protocol.HIT_REQ):
            return
        print('Server: Received hit request, sending response')
        conn.send(Hasher.enhash(Protocol.HIT_RES))
        print('Server: Sent hit response')
        data = conn.recv(Protocol.BUFFER_SIZE)
        print(f'Server: got {data}')
        player = player_handler.get_player(data.decode(Protocol.ENCODING).strip())
        if player is None:
            print(f"player {data.strip()} not known")
            return
        print('Server: doing damage')
        player['health'] = player['health'] - 5
        player_handler.update_player(player)

