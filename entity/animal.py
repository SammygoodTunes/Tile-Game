
import pygame
from enum import Enum


class Movements(Enum):
    DOWN, RIGHT, UP, LEFT = range(3, -1, -1)


class Animal(pygame.sprite.Sprite):

    def __init__(self, x=0, y=0, speed=5):
        super().__init__()
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.asset = None
        self.speed = speed
        self.move = 0

    def events(self, e):
        pass

    def update(self):
        # if self.is_moving_left():
        #     self.x -= self.speed
        # if self.is_moving_up():
        #     self.y -= self.speed
        # if self.is_moving_right():
        #     self.x += self.speed
        # if self.is_moving_down():
        #     self.y += self.speed
        pass

    def draw(self, screen):
        pass
