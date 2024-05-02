
from hashlib import sha256

from game.network.protocol import Protocol


class Hasher:

    @staticmethod
    def hash(packet: str) -> str:
        return sha256(packet.encode(Protocol.ENCODING)).hexdigest()

    @staticmethod
    def enhash(packet: str) -> bytes:
        return sha256(packet.encode(Protocol.ENCODING)).hexdigest().encode(Protocol.ENCODING)
