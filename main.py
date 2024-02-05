# !/usr/local/bin/python
# -*- coding: utf-8 -*-

from core.catchncage import Game
from pygame import init, quit
import pyautogui
import faulthandler


def main():

    faulthandler.enable()

    init()
    width = pyautogui.size()[0] // 4
    height = width / 12 * 8
    game = Game(width, height)

    while game.is_running():
        game.update()

    quit()


if __name__ == '__main__':
    main()
