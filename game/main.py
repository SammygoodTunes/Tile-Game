# !/usr/local/bin/python
# -*- coding: utf-8 -*-

'''

    Project: Tile Game
    Version: 0.0.1a
    Author: SammygoodTunes
    Art: Pickmonde, SammygoodTunes

'''

import faulthandler
from pygame import init, quit, display

from game.core.game import Game


def main():

    faulthandler.enable()

    init()
    width = display.Info().current_w // 3
    height = width / 12 * 8

    game = Game(width, height)

    while game.is_running():
        game.update()

    quit()


if __name__ == '__main__':
    main()
