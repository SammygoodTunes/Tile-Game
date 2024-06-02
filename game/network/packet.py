import pickle
from hashlib import sha256
import lzma

from game.network.protocol import Protocol
from game.utils.logger import logger


class Hasher:
    """
    Class for hashing packets.
    Used for sending and receiving protocol commands from the client/server.
    """

    @staticmethod
    def hash(packet: str) -> str:
        """
        Hash a packet.
        """
        return sha256(packet.encode(Protocol.ENCODING)).hexdigest()

    @staticmethod
    def enhash(packet: str) -> bytes:
        """
        Hash and encode (Protocol.ENCODING) a packet.
        """
        return sha256(packet.encode(Protocol.ENCODING)).hexdigest().encode(Protocol.ENCODING)


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
