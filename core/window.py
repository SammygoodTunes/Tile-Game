
import pygame
import pyautogui
import data.data_manager as data_mng
from gui.label import Label
from gui.screen_manager import Screens
from time import time


class Window:

    FONT_PATH = "assets/font.ttf"

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.old_width = width
        self.old_height = height
        (self.max_width,
         self.max_height) = pyautogui.size()
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        self.fps_cap = 200
        self.clock = pygame.time.Clock()
        self.time = time()
        self.seconds = 0
        self.font = pygame.font.Font(Window.FONT_PATH, 11)
        self.screens = Screens(self)
        self.fps_label = (Label(f"FPS: {str(round(self.clock.get_fps()))}", self.width - 75, -8)
                          .set_shadow_x(self.width - 73).set_shadow_y(-6)
                          .set_colour((240, 240, 240)).set_shadow_colour((25, 25, 25)))
        self.paused = False
        self.start_game = False
        self.fullscreen = False
        self.halt_refresh = False # used to prevent graphical distortion when resizing window
        pygame.display.set_caption(data_mng.get_game_property(data_mng.APP_NAME))

    def get_time_in_seconds(self):
        return int(time() - self.time)

    def clear(self, colour):
        self.screen.fill(colour, (0, 0, self.width, self.height))

    def tick(self):
        if self.halt_refresh:
            self.halt_refresh = False
            return
        pygame.display.flip()
        self.clock.tick(self.fps_cap)

    def resize(self, e):
        self.halt_refresh = True
        if pygame.version.vernum >= (2, 0):
            self.screen = pygame.display.get_surface()
            self.width, self.height = self.screen.get_size()
        else:
            self.width, self.height = e.w, e.h
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE | pygame.DOUBLEBUF)

    def draw_fps(self):
        if self.screens.options_screen.show_fps_box.is_checked():
            if self.seconds != self.get_time_in_seconds():
                self.fps_label.set_text(f"FPS: {str(round(self.clock.get_fps()))}")
                self.seconds = self.get_time_in_seconds()
            self.fps_label.draw(self.screen)

    def update_ui(self):
        self.fps_label.set_auto_font_size(self.width, self.height, self.max_width, self.max_height)
        self.fps_label.set_x(self.width - (self.fps_label.get_font_size() * 7) - 4).set_shadow_x(self.width - (self.fps_label.get_font_size() * 7) - 4 - 2)
        self.fps_label.set_y(-self.fps_label.get_font_size() + 4).set_shadow_y(-self.fps_label.get_font_size() + 6)
        self.screens.update_ui()

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.old_width = self.width
            self.old_height = self.height
            self.width, self.height = pyautogui.size()
        else:
            self.width = self.old_width
            self.height = self.old_height
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN if self.fullscreen else pygame.RESIZABLE)
