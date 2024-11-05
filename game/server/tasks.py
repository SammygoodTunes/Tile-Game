"""
Module name: tasks

This module defines all the server-side tasks when a connection is being established with a client, or whilst a
client is connected.
These tasks check the authenticity of the client and any potential errors, as well as send various required packets
of game data, requests and responses. These packets are built using the different packet builders.

(See network/builders for the different packet builders.)
(See network/protocol for the different requests and responses.)
"""

from math import ceil

from game.data.properties.server_properties import ServerProperties
from game.network.builders.base_builder import BaseBuilder
from game.network.builders.player_builder import PlayerBuilder
from game.network.packet import Hasher, Compressor, Packet, fill, to_bytes, hex_len
from game.network.protocol import Protocol
from game.server.handlers.player_handler import PlayerHandler
from game.server.handlers.world_handler import WorldHandler
from game.utils.logger import logger


class ServerTasks:
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
            logger.info(f'Sending recognition message to {addr}')
            conn.send(Hasher.enhash(Protocol.RECOGNITION_RES))
            return True
        return False

    @staticmethod
    def map_data(conn, addr, world_handler: WorldHandler) -> None:
        """
        Task for sending map data to a client.
        """
        data = conn.recv(Protocol.BUFFER_SIZE)
        if data and data == Hasher.enhash(Protocol.MAPDATA_REQ):
            logger.info(f'Sending map to {addr}')
            compressed_data_obj = Compressor.compress(world_handler.get_map_data())
            conn.send(Hasher.enhash(Protocol.MAPDATA_RES))
            conn.send(fill(compressed_data_obj))
            conn.send(Hasher.enhash(Protocol.MAPDATA_EOS))
            logger.info(f'Sent!')

    @staticmethod
    def player_join(conn, player_handler: PlayerHandler) -> str:
        """
        Task for joining a client player to the server.
        Returns the received player name.
        """
        data = conn.recv(Protocol.BUFFER_SIZE)
        if not data or data == Hasher.enhash(Protocol.PLAYERJOIN_REQ):
            conn.send(Hasher.enhash(Protocol.PLAYERJOIN_RES))
        data = conn.recv(Protocol.BUFFER_SIZE)
        if not data:
            return str()
        player_name = data.decode(Protocol.ENCODING)
        player_dict = PlayerBuilder.create_player()
        player_dict[PlayerBuilder.NAME_KEY] = player_name
        if player_handler.get_player(player_name)['index'] is not None:
            conn.send(Hasher.enhash(Protocol.NAMEALREXIST_ERR))
            return str()
        if len(player_handler.get_players()) >= ServerProperties.MAX_PLAYERS:
            conn.send(Hasher.enhash(Protocol.MAXPLAYERS_ERR))
            return str()
        player_handler.track_player(player_dict)
        conn.send(Hasher.enhash(Protocol.PLAYEROBJ_RES))
        return player_name

    @staticmethod
    def local_game_state(conn):
        """
        Task for requesting a local game state. This is only for specific needs like player data.
        """
        conn.send(Hasher.enhash(Protocol.LCGAME_REQ))

    @staticmethod
    def game_state(conn, data: bytes, player_handler: PlayerHandler, world_handler: WorldHandler) -> bool:
        """
        Task for sending the overall game state to a client.
        """
        if not data or data != Hasher.enhash(Protocol.GLGAME_REQ):
            return False
        conn.send(Hasher.enhash(Protocol.GLGAME_RES))
        compressed_players_obj = player_handler.get_players(compressed=True)
        compressed_map_data_obj = Compressor.compress(world_handler.get_map_data())
        data = int.to_bytes(len(compressed_players_obj)) + compressed_players_obj + compressed_map_data_obj
        packet = fill(hex_len(data) + data)
        packet = hex_len(packet) + packet[Packet.DATA_SIZE:]
        conn.send(packet)
        return True

    @staticmethod
    def incoming_packets(conn, data: bytes, player_handler: PlayerHandler, world_handler: WorldHandler) -> bool:
        """
        Task for handling incoming packets.
        Return True if packet is received and is valid, otherwise False
        """
        if not data or data[:len(Protocol.SPACKET_MAGIC)] != to_bytes(Protocol.SPACKET_MAGIC):
            return False
        length = int.from_bytes(data[len(Protocol.SPACKET_MAGIC):len(Protocol.SPACKET_MAGIC) + Packet.DATA_SIZE])
        if not length:
            return False
        packet = b''
        data = data[len(Protocol.SPACKET_MAGIC) + Packet.DATA_SIZE:len(Protocol.SPACKET_MAGIC) + Packet.DATA_SIZE + length]
        for i in range(ceil(length / Protocol.BUFFER_SIZE)):
            if i != 0:
                data = conn.recv(Protocol.BUFFER_SIZE)
            packet += data
        decompressed_packet = PlayerBuilder.get_decompressed_player_packet(packet)
        type_id = packet[0] - BaseBuilder.COMMAND_ID_OFFSET
        conn.send(Hasher.enhash(Protocol.PACKETRECV_RES))
        if type_id == BaseBuilder.PLAYER_POSITION_UPDATE_COMMAND:
            player_handler.update_player_position(decompressed_packet)
        elif type_id == BaseBuilder.PLAYER_TILE_BREAK_COMMAND:
            world_handler.update_broken_tile(decompressed_packet)
        return True

