"""
Module name: logger

This module defines the logger.
"""

from numpy import ceil, log2
from os import path
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
    return path.join(path.abspath("."), directory)
