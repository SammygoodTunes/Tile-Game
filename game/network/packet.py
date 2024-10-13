import pickle
from hashlib import shake_256
import lzma

from game.network.protocol import Protocol
from game.utils.logger import logger


class Packet:
    """
    Class for determining the properties of the packet header.
    """
    DATA_SIZE = 4


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
        return None


def fill(data: bytes) -> bytes:
    """
    Fill the packet with empty data if its size is not a multiple of BUFFER_SIZE.
    """
    return data + b' ' * (Protocol.BUFFER_SIZE - len(data) % Protocol.BUFFER_SIZE)


def to_bytes(data: str) -> bytes:
    """
    Return string as bytes encoded with protocol's chosen encoding.
    """
    return bytes(data, encoding=Protocol.ENCODING)

def hex_len(data: bytes) -> bytes:
    """
    Return length of data in hex. Used in packet header for determining data size. Max length is of SIZE / 2 bytes.
    """
    return to_bytes(f'{len(data):0{Packet.DATA_SIZE}x}')
