
from numpy import ceil, log2
from typing import SupportsFloat, SupportsIndex

def c_log2(x: SupportsFloat | SupportsIndex, /) -> int:
    return int(ceil(log2(x)))
