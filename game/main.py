# !/usr/local/bin/python
# -*- coding: utf-8 -*-

"""
Project: Tile Game
Version: 0.0.1a
Author: SammygoodTunes
Art: Pickmonde, SammygoodTunes
"""

import argparse
import faulthandler
from pygame import init, quit, display

from game.core.game import Game
from game.utils.logger import logger


def main() -> None:
    """
    Here is where it all begun...
    """
    faulthandler.enable()

    init()

    width: int = display.Info().current_w // 3
    height: int = width // 12 * 8
    game: Game = Game(width, height)

    while game.is_running():
        game.update()

    quit()


if __name__ == '__main__':
    logger.debug('Starting game...')
    main()
