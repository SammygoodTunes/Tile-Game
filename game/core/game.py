
from math import sin
import pygame

from game.core.window import Window
from game.entity.player import Player
from game.world.camera import Camera
from game.world.world import World


class Game(Window):

    def __init__(self, window_width=1366, window_height=768):
        super().__init__(window_width, window_height)
        self._running = True
        self.screens.link_game(self)
        self.camera = Camera(self, speed=350)
        self.player = Player(self, speed=350)
        self.world = World(self)
        self.update_all_uis()

    def update(self):
        ticks = pygame.time.get_ticks()
        if self.start_game and self.world.get_map().is_ready():
            self.clear((140, 150, 235))
            self.world.draw(self.screen)
            # self.world.draw_wireframe(self.screen)
            self.player.draw(self.screen)
            self.player.draw_selection_grid(self.screen)
            self.player.draw_ui(self.screen)
            
            self.player.update(self, self.world.get_map())
            self.world.update(self, self.player)
        else:
            self.clear((round(20 * sin(ticks / 5000) + 150), 
                        round(10 * sin(ticks / 2500) + 120),
                        235))
        self.all_events()
        self.screens.update()
        self.draw_fps() 
        self.tick()

    # Used for when game needs to be updated during threaded process
    # This should be used in a while loop controlled by an Event()
    def update_loop(self):
        self.all_events()
        self.screens.update()
        self.draw_fps()
        self.tick()

    def all_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.stop()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN and pygame.key.get_mods() & pygame.KMOD_ALT:
                    self.toggle_fullscreen()
                    self.resize(e)
                    self.update_all_uis()
            if e.type == pygame.VIDEORESIZE:
                self.resize(e)
                self.update_all_uis()
                continue
            if e.type == pygame.VIDEOEXPOSE:
                self.update_all_uis()
            if not self.paused and self.start_game and self.world.get_map().is_ready():
                self.player.events(e)
            self.screens.events(e)
        if not self.paused:
            self.camera.events()

    def update_all_uis(self):
        self.update_ui()
        self.player.update_ui()
        self.world.update_ui()

    def is_running(self):
        return self._running
    
    def stop(self):
        self._running = False
