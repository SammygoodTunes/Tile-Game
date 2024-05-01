
from math import sin
import pygame

from game.data.data_manager import verify_game_property_values
from game.core.window import Window
from game.entity.player import Player
from game.utils.logger import logger
from game.world.camera import Camera
from game.world.world import World


class Game(Window):
    """
    Class for managing a game instance.
    """

    def __init__(self, window_width: int, window_height: int) -> None:
        super().__init__(window_width, window_height)
        self._running: bool = True
        self.screens.link_game(self)
        self.camera: Camera = Camera(speed=350)
        self.player: Player = Player(speed=350)
        self.world: World = World()
        self.player.init(self)
        self.update_all_uis()
        verify_game_property_values()
        logger.debug(f'Created {__class__.__name__} with attributes {self.__dict__}')

    def update(self) -> None:
        """
        Update all child objects and core of the game.
        """
        ticks = pygame.time.get_ticks()
        if self.start_game and self.world.get_map().is_ready():
            self.clear((140, 150, 235))
            self.world.draw(self)
            # self.world.draw_wireframe(self.screen)
            self.player.draw(self)
            self.player.draw_selection_grid(self)
            self.player.main_hud.draw()
            
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
    def update_loop(self) -> None:
        """
        Like the standard update loop, but only used for threaded tasks.
        """
        self.all_events()
        self.screens.update()
        self.draw_fps()
        self.tick()

    def all_events(self) -> None:
        """
        Verify for any potential pygame events and update the targeted elements accordingly.
        """
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.stop()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN and pygame.key.get_mods() & pygame.KMOD_ALT:
                    self.toggle_fullscreen()
            if e.type == pygame.VIDEORESIZE:
                self.resize(e)
                self.update_all_uis()
                continue
            if e.type == pygame.VIDEOEXPOSE:
                self.update_all_uis()
            if not self.paused and self.start_game and self.world.get_map().is_ready():
                self.player.events(self, e)
            self.screens.events(e)
        if not self.paused:
            self.camera.events(self)

    def update_all_uis(self) -> None:
        """
        Update all the GUI-related elements.
        """
        self.update_ui()
        self.player.update_ui(self)
        self.world.update_ui()

    def is_running(self) -> bool:
        """
        Return the running state of the game.
        """
        return self._running

    def is_debug_mode_enabled(self) -> bool:
        """
        Return the state of the game's debug mode.
        """
        return self._debug
    
    def stop(self) -> None:
        """
        Terminate the game.
        """
        self._running = False
