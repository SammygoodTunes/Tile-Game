import pickle
from hashlib import sha256
from pickle import dumps, loads
import lzma

from game.network.protocol import Protocol


class Hasher:

    @staticmethod
    def hash(packet: str) -> str:
        return sha256(packet.encode(Protocol.ENCODING)).hexdigest()

    @staticmethod
    def enhash(packet: str) -> bytes:
        return sha256(packet.encode(Protocol.ENCODING)).hexdigest().encode(Protocol.ENCODING)


class Compressor:

    @staticmethod
    def compress(obj: any) -> bytes:
        return lzma.compress(pickle.dumps(obj))

    @staticmethod
    def decompress(data: bytes) -> any:
        return pickle.loads(lzma.decompress(data))
