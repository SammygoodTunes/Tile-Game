# !/usr/local/bin/python
# -*- coding: utf-8 -*-

"""
Project: Tile Game
Version: 0.0.1a
Author: SammygoodTunes
Art: Pickmonde, Jatzylap, SammygoodTunes
"""

import faulthandler
import cProfile
import io
import pstats
import sys
from pstats import SortKey

from pygame import init, quit, display
from traceback import format_exc

from game.core.game import Game
from game.utils.logger import logger


def main() -> None:
    """
    Here is where it all begun...
    """
    faulthandler.enable()

    # pr = cProfile.Profile()
    # pr.enable()

    init()

    width: int = display.Info().current_w // 3
    height: int = width // 12 * 8
    game: Game = Game(width, height)

    try:
        while game.is_running():
            game.update()
    except Exception:
        game.crash(format_exc())

    quit()

    #pr.disable()

    # s = io.StringIO()
    # sortby = SortKey.CUMULATIVE
    # ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    # ps.print_stats()
    # print(s.getvalue())


if __name__ == '__main__':
    if sys.stderr is None:
        stream = io.StringIO()
        sys.stdout = stream
        sys.stderr = stream
    logger.info('Starting game...')
    main()
    logger.info('Closing game...')
