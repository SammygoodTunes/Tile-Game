"""
Module name: packet

This module defines a set of methods for hashing, compressing and altering data packets.
"""


import pickle
from hashlib import shake_256
import lzma

from game.network.protocol import Protocol
from game.utils.logger import logger


class Packet:
    """
    Class for determining the properties of the packet header.
    """
    DATA_SIZE = 2


class Hasher:
    """
    Class for hashing packets.
    Used for sending and receiving protocol commands from the client/server.
    """

    @staticmethod
    def hash(packet: str) -> str:
        """
        Hash a packet and return hash of size BUFFER_SIZE.
        """
        return shake_256(packet.encode(Protocol.ENCODING)).hexdigest(Protocol.BUFFER_SIZE // 2)

    @staticmethod
    def enhash(packet: str) -> bytes:
        """
        Hash and encode (Protocol.ENCODING) a packet.
        Return hash of size BUFFER_SIZE.
        """
        return shake_256(packet.encode(Protocol.ENCODING)).hexdigest(Protocol.BUFFER_SIZE // 2).encode(Protocol.ENCODING)


class Compressor:
    """
    Class for compressing objects.
    Used for sending and receiving game data from the client/server.
    """

    @staticmethod
    def compress(obj: any) -> bytes:
        """
        Compress an object to bytes.
        """
        return lzma.compress(pickle.dumps(obj))

    @staticmethod
    def decompress(data: bytes) -> any:
        """
        Decompress byte data to an object, if valid.
        Otherwise, return None.
        """
        try:
            return pickle.loads(lzma.decompress(data))
        except lzma.LZMAError as e:
            logger.error(f'Could not decompress: {e}')
            raise ConnectionRefusedError


def fill(data: bytes) -> bytes:
    """
    Fill the packet with empty data if its size is not a multiple of BUFFER_SIZE.
    """
    empty_data_size = Protocol.BUFFER_SIZE - len(data) % Protocol.BUFFER_SIZE
    if empty_data_size == Protocol.BUFFER_SIZE:
        return data
    return data + b' ' * empty_data_size


def to_bytes(data: str) -> bytes:
    """
    Return string as bytes encoded with protocol's chosen encoding.
    """
    return bytes(data, encoding=Protocol.ENCODING)

def hex_len(data: bytes) -> bytes:
    """
    Return length of data in hex. Used in packet header for determining data size.
    """
    return int.to_bytes(len(data), length=Packet.DATA_SIZE)
