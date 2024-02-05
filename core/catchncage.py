
from core.window import Window
from entity.animal import Animal
from entity.player import Player
from world.world import World
from world.camera import Camera
import pygame


class Game(Window):

    def __init__(self, window_width=1366, window_height=768):
        super().__init__(window_width, window_height)
        self._running = True
        self.screens.link_game(self)
        self.camera = Camera(self, speed=360)
        self.player = Player(self, speed=350, x=0, y=0)
        self.world = World(self)
        self.update_all_uis()

    def update(self):
        self.clear()
        if self.start_game:
            self.world.draw(self.screen)
            # self.world.draw_wireframe(self.screen)
            # self.player.draw_selection_grid(self.screen)
            self.player.draw(self.screen)
            self.player.draw_score(self.screen)
            self.player.draw_position(self.screen)
            self.player.draw_hotbar(self.screen)
            self.player.draw_ui(self.screen)
            
            if not self.paused:
                self.player.update(self, self.world.get_map())
                self.world.update(self, self.player)
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
