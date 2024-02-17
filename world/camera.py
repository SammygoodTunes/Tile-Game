
import pygame
from utils.tools import clamp

class Camera:

    # Camera position strictly relative to
    # the center of the screen

    VELOCITY_STEP_START = 5
    VELOCITY_STEP_STOP = 3.5
    VELOCITY_THRESHOLD = 0.001

    def __init__(self, game, x=0, y=0, speed=50):
        self.game = game
        self.x = 0
        self.y = 0
        self.speed = speed
        self.velocity_x = 0
        self.velocity_y = 0

    def events(self):
        d: float = self.game.clock.get_time() / 1000.0
        keys = pygame.key.get_pressed()

        #print(self.game.player.get_coefficient_from_center_x(), self.game.player.get_coefficient_from_center_y())

        if self.velocity_x != 0:
            self.x += self.speed * self.game.player.get_coefficient_from_center_x() * self.velocity_x * d
        if self.velocity_y != 0:
            self.y += self.speed * self.game.player.get_coefficient_from_center_y() * self.velocity_y * d

        if self.game.player.is_near_left_edge():
            self.velocity_x = clamp(self.velocity_x - Camera.VELOCITY_STEP_START * d, -1, 1)
        elif self.game.player.is_near_right_edge():
            self.velocity_x = clamp(self.velocity_x + Camera.VELOCITY_STEP_START * d, -1, 1)
        if self.game.player.is_near_top_edge():
            self.velocity_y = clamp(self.velocity_y - Camera.VELOCITY_STEP_START * d, -1, 1)
        elif self.game.player.is_near_bottom_edge():
            self.velocity_y = clamp(self.velocity_y + Camera.VELOCITY_STEP_START * d, -1, 1)
        
        if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            if -Camera.VELOCITY_STEP_STOP * d < self.velocity_x < Camera.VELOCITY_STEP_STOP * d and self.velocity_x != 0:
                self.velocity_x = 0
            elif self.velocity_x > 0:
                self.velocity_x = clamp(self.velocity_x - Camera.VELOCITY_STEP_STOP * d, 0, 1)
            elif self.velocity_x < 0:
                self.velocity_x = clamp(self.velocity_x + Camera.VELOCITY_STEP_STOP * d, -1, 0)

        if not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            if -Camera.VELOCITY_STEP_STOP * d < self.velocity_y < Camera.VELOCITY_STEP_STOP * d and self.velocity_y != 0:
                self.velocity_y = 0
            elif self.velocity_y > 0:
                self.velocity_y = clamp(self.velocity_y - Camera.VELOCITY_STEP_STOP * d, 0, 1)
            elif self.velocity_y < 0:
                self.velocity_y = clamp(self.velocity_y + Camera.VELOCITY_STEP_STOP * d, -1, 0)
