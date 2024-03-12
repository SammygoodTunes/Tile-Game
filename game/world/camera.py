
from pygame import K_UP, K_DOWN, K_LEFT, K_RIGHT
from pygame import key
from pygame.math import clamp


# Camera position strictly relative to the center of the screen

class Camera:

    VELOCITY_STEP_START = 5
    VELOCITY_STEP_STOP = 3.5
    VELOCITY_THRESHOLD = 0.001

    def __init__(self, speed=50):
        self.x = 0
        self.y = 0
        self.speed = speed
        self.velocity_x = 0
        self.velocity_y = 0

    def events(self, game):
        d: float = game.clock.get_time() / 1000.0
        keys = key.get_pressed()

        if self.velocity_x != 0:
            self.x += self.speed * game.player.get_coefficient_from_center_x(game) * self.velocity_x * d
        if self.velocity_y != 0:
            self.y += self.speed * game.player.get_coefficient_from_center_y(game) * self.velocity_y * d

        if game.player.is_near_left_edge():
            self.velocity_x = clamp(self.velocity_x - Camera.VELOCITY_STEP_START * d, -1, 1)
        elif game.player.is_near_right_edge():
            self.velocity_x = clamp(self.velocity_x + Camera.VELOCITY_STEP_START * d, -1, 1)
        if game.player.is_near_top_edge():
            self.velocity_y = clamp(self.velocity_y - Camera.VELOCITY_STEP_START * d, -1, 1)
        elif game.player.is_near_bottom_edge():
            self.velocity_y = clamp(self.velocity_y + Camera.VELOCITY_STEP_START * d, -1, 1)
        
        if not keys[K_LEFT] and not keys[K_RIGHT]:
            if -Camera.VELOCITY_STEP_STOP * d < self.velocity_x < Camera.VELOCITY_STEP_STOP * d and self.velocity_x != 0:
                self.velocity_x = 0
            elif self.velocity_x > 0:
                self.velocity_x = clamp(self.velocity_x - Camera.VELOCITY_STEP_STOP * d, 0, 1)
            elif self.velocity_x < 0:
                self.velocity_x = clamp(self.velocity_x + Camera.VELOCITY_STEP_STOP * d, -1, 0)

        if not keys[K_UP] and not keys[K_DOWN]:
            if -Camera.VELOCITY_STEP_STOP * d < self.velocity_y < Camera.VELOCITY_STEP_STOP * d and self.velocity_y != 0:
                self.velocity_y = 0
            elif self.velocity_y > 0:
                self.velocity_y = clamp(self.velocity_y - Camera.VELOCITY_STEP_STOP * d, 0, 1)
            elif self.velocity_y < 0:
                self.velocity_y = clamp(self.velocity_y + Camera.VELOCITY_STEP_STOP * d, -1, 0)

    def reset(self):
        self.x = self.y = self.velocity_x = self.velocity_y = 0
