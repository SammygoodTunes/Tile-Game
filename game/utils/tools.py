"""
Module name: logger

This module defines the logger.
"""

from math import ceil, log2
from os import path
from pathlib import Path
import sys
from typing import SupportsFloat, SupportsIndex


def c_log2(x: SupportsFloat | SupportsIndex, /) -> int:
    """
    Return cast int ceiling log2 of the given value.
    """
    return int(ceil(log2(x)))


def resource_dir(directory: str):
    """
    Return the correct resource path of a resource directory.
    """
    if getattr(sys, 'frozen', False):
        return path.join(sys._MEIPASS, directory)
    return path.join(Path(__file__).parent.parent.parent, directory)
