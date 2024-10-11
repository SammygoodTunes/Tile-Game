
from numpy import ceil, log2
from os import path
import sys
from typing import SupportsFloat, SupportsIndex

def c_log2(x: SupportsFloat | SupportsIndex, /) -> int:
    return int(ceil(log2(x)))

def resource_dir(directory: str):
    if getattr(sys, 'frozen', False):
        return path.join(sys._MEIPASS, directory)
    return path.join(path.abspath("."), directory)
