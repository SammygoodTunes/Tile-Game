# !/usr/local/bin/python
# -*- coding: utf-8 -*-

# Project: Tile Game
# Version: 0.0.1a 
# Author: SammygoodTunes
# Art: Pickmonde, SammygoodTunes

from game.core.game import Game
from pygame import init, quit, display
import faulthandler


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
