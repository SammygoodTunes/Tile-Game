
import math
import pygame
from pygame.math import clamp
from random import randint
from typing import Self

from game.data.items.items import Items
from game.data.keys import Keys
from game.data.properties.player_properties import PlayerProperties
from game.data.properties.tile_properties import TileProperties
from game.data.states.mouse_states import MouseStates
from game.data.states.player_states import PlayerStates
from game.data.tiles.tiles import Tiles
from game.data.tiles.tile import Tile
from game.data.tiles.tile_types import TileTypes
from game.gui.screens.main_hud import MainHud
from game.network.builders.base_builder import BaseBuilder
from game.network.builders.player_builder import PlayerBuilder
from game.utils.exceptions import ZeroOrLessSpawnPlayerAttempts
from game.utils.logger import logger
from game.world.camera import Camera
from game.world.map_manager import Map


class Player:
    """
    Class for creating a player.
    """

    TIMERS_COUNT: int = 2
    MINING_TIMER: int = 0
    DAMAGE_TIMER: int = 1

    def __init__(self, x: int = 0, y: int = 0, speed: int = 50) -> None:
        self.asset: pygame.surface.Surface | None = None
        self._x: int = x
        self._y: int = y
        self.screen_x: int = x
        self.screen_y: int = y
        self.width: int = 32
        self.height: int = 32
        self.velocity_x: float = 0.0
        self.velocity_y: float = 0.0
        self.speed: int = speed
        self.move: int = 0
        self.selected_tile_x: int = 0
        self.selected_tile_y: int = 0
        self.selected_tile_sx: int = 0
        self.selected_tile_sy: int = 0
        self.breaking_tile: tuple[int, int] | None = None
        self.breaking: bool = False
        self.hurt: bool = False
        self.prev_selected_tile: tuple[int, int] = (0, 0)
        self.prev_broken_tile: tuple[int, int] = (0, 0)
        self.score: int = 0
        self.health: int = 100
        self.edges = [False, False, False, False]
        self.timers: list[float] = [0.0] * Player.TIMERS_COUNT
        self.main_hud = None
        self.player_name = str()

    def init(self, game) -> None:
        """
        Define the player attributes that depend on the given game object.
        """
        self.main_hud = MainHud(game)
        self.main_hud.set_state(True)

    def events(self, game, map_obj, e: pygame.event.Event | pygame.event.EventType) -> None:
        """
        Handle the player events.
        """
        if e.type == pygame.MOUSEWHEEL:
            self.main_hud.hotbar.unselect_slot(self.main_hud.hotbar.get_selected_slot())
            self.main_hud.hotbar.select_slot((self.main_hud.hotbar.get_selected_slot() - e.y) % len(self.main_hud.hotbar.get_slots()))
            self.main_hud.hotbar.init_slots()
            self.main_hud.hotbar.update(game)
        tile_x, tile_y = self.selected_tile_x, self.selected_tile_y
        if not 0 <= tile_x < map_obj.get_width_in_tiles() or not 0 <= tile_y < map_obj.get_height_in_tiles():
            return
        if map_obj.get_dynatile(tile_x, tile_y) or not map_obj.get_tile(tile_x, tile_y) in TileTypes.BREAKABLE:
            return
        if e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == MouseStates.LMB:
                self.breaking = True
                self.timers[Player.MINING_TIMER] = pygame.time.get_ticks() / 1000.0
                map_obj.tile_manager.draw(
                    self.selected_tile_x * TileProperties.TILE_SIZE,
                    self.selected_tile_y * TileProperties.TILE_SIZE,
                    map_obj.get_tile(self.selected_tile_x, self.selected_tile_y),
                    map_obj.get_dynatile_surface()
                )
        elif e.type == pygame.MOUSEBUTTONUP:
            if e.button == MouseStates.LMB:
                self.breaking = False
                self.timers[Player.MINING_TIMER] = pygame.time.get_ticks() / 1000.0
                map_obj.tile_manager.draw(
                    self.selected_tile_x * TileProperties.TILE_SIZE,
                    self.selected_tile_y * TileProperties.TILE_SIZE,
                    map_obj.get_tile(self.selected_tile_x, self.selected_tile_y),
                    map_obj.get_dynatile_surface()
                )

    def draw(self, game) -> None:
        """
        Draw the player to the screen.
        """
        if not self.is_dead():
            self.screen_x = game.width / 2 - game.client.camera.x + self._x
            self.screen_y = game.height / 2 - game.client.camera.y + self._y
            if self.is_in_lava(game.client.world.get_map()):
                pygame.draw.rect(game.screen, (220, 200, 200), (self.screen_x, self.screen_y, self.width, self.height))
                return
            if self.is_in_water(game.client.world.get_map()):
                pygame.draw.rect(game.screen, (200, 200, 220), (self.screen_x, self.screen_y, self.width, self.height))
                return
            pygame.draw.rect(game.screen, (255, 255, 255), (self.screen_x, self.screen_y, self.width, self.height))

        # screen.blit(self.asset, (self.screen_x, self.screen_y, self.width, self.height))

    def draw_selection_grid(self, game) -> None:
        """
        Draw the player tile selection grid to the screen.
        """
        if game.paused or self.is_dead() or self.main_hud.hotbar.get_selected_slot_item() != Items.SHOVEL:
            return
        _map = game.client.world.get_map()
        mx, my = pygame.mouse.get_pos()
        center_x, center_y = game.width // 2, game.height // 2
        map_width, map_height = _map.get_width_in_tiles(), _map.get_height_in_tiles()

        wx, wy = (round(game.client.camera.x) - (center_x - mx)) // 32, (round(game.client.camera.y) - (center_y - my)) // 32

        selected_tile_x = wx + map_width // 2
        selected_tile_y = wy + map_height // 2

        self.selected_tile_sx, self.selected_tile_sy = _map.tile_to_screen_pos(
            game, selected_tile_x, selected_tile_y
        )

        self.selected_tile_x = selected_tile_x
        self.selected_tile_y = selected_tile_y

        if not 0 <= self.selected_tile_x < _map.get_width_in_tiles() or not 0 <= self.selected_tile_y < _map.get_height_in_tiles():
            return
        if not self.has_selected_breakable(game.client.world.get_map()) or self.is_selected_breakable_obstructed(game.client.world.get_map()):
            return

        colour_anim: int = round(127.5 * math.sin(pygame.time.get_ticks() / 128) + 127.5)
        pygame.draw.rect(game.screen, (255, colour_anim, colour_anim), (
            self.selected_tile_sx,
            self.selected_tile_sy,
            TileProperties.TILE_SIZE,
            TileProperties.TILE_SIZE
        ), 2, 4)

    def draw_gun_pointer(self, game):
        if game.paused or self.is_dead() or self.main_hud.hotbar.get_selected_slot_item() != Items.GUN:
            return
        mx, my = pygame.mouse.get_pos()
        offset_x, offset_y = mx - self.screen_x - 16, my - self.screen_y - 16
        length = int(math.sqrt(offset_x ** 2 + offset_y ** 2))
        if length == 0:
            return
        slope_x, slope_y = offset_x / length, offset_y / length
        line_length = 16
        for i in range(0, length // line_length, 2):
            if i > 7:
                break
            colour_anim: int = round(127.5 * math.sin((pygame.time.get_ticks() - i * 10) / 64) + 127.5)
            pygame.draw.line(game.screen,(255, colour_anim // 2, colour_anim // 2),(
                    self.screen_x + 16 + (slope_x * i * line_length),
                    self.screen_y + 16 + (slope_y * i * line_length)
                ),(
                    self.screen_x + 16 + (slope_x * (i + 1) * line_length),
                    self.screen_y + 16 + (slope_y * (i + 1) * line_length)
                ), 2
            )

    def update(self, game, map_obj: Map) -> None:
        """
        Update the player.
        """
        if self.is_dead():
            game.screens.gameover_screen.set_state(not game.paused)
            return
        d: float = game.clock.get_time() / 1000.0
        prev_x: int = self._x
        prev_y: int = self._y

        speed: int
        if self.is_in_water(map_obj):
            speed = PlayerProperties.SPEED_IN_WATER
        elif self.is_in_lava(map_obj):
            speed = PlayerProperties.SPEED_IN_LAVA
        else:
            speed = PlayerProperties.SPEED

        tile_x, tile_y = map_obj.get_tile_pos(self._x, self._y)
        tile_wx, tile_wy = map_obj.tile_to_world_pos(tile_x, tile_y)
        walls = self.get_walls(map_obj)
        keys = pygame.key.get_pressed()

        if not game.paused and game.focused:
            self.move = self.move | (1 << PlayerStates.MOVE_LEFT) if keys[Keys.MOVE_LEFT] else self.move & ~(1 << PlayerStates.MOVE_LEFT)
            self.move = self.move | (1 << PlayerStates.MOVE_UP) if keys[Keys.MOVE_UP] else self.move & ~(1 << PlayerStates.MOVE_UP)
            self.move = self.move | (1 << PlayerStates.MOVE_RIGHT) if keys[Keys.MOVE_RIGHT] else self.move & ~(1 << PlayerStates.MOVE_RIGHT)
            self.move = self.move | (1 << PlayerStates.MOVE_DOWN) if keys[Keys.MOVE_DOWN] else self.move & ~(1 << PlayerStates.MOVE_DOWN)
        else:
            self.move = 0

        if self.velocity_x != 0:
            self._x += round(speed * self.velocity_x * d, 2)
        if self.velocity_y != 0:
            self._y += round(speed * self.velocity_y * d, 2)

        if self.is_moving_left():
            self.velocity_x = clamp(self.velocity_x - d / PlayerProperties.VELOCITY_START_DURATION, -1, 1)
        if self.is_moving_right():
            self.velocity_x = clamp(self.velocity_x + d / PlayerProperties.VELOCITY_START_DURATION, -1, 1)
        if self.is_moving_up():
            self.velocity_y = clamp(self.velocity_y - d / PlayerProperties.VELOCITY_START_DURATION, -1, 1)
        if self.is_moving_down():
            self.velocity_y = clamp(self.velocity_y + d / PlayerProperties.VELOCITY_START_DURATION, -1, 1)

        if not self.is_moving_left() and not self.is_moving_right():
            if -PlayerProperties.VELOCITY_THRESHOLD < self.velocity_x < PlayerProperties.VELOCITY_THRESHOLD and self.velocity_x != 0:
                self.velocity_x = 0
            if self.velocity_x > 0:
                self.velocity_x = clamp(self.velocity_x - d / PlayerProperties.VELOCITY_STOP_DURATION, 0, 1)
            elif self.velocity_x < 0:
                self.velocity_x = clamp(self.velocity_x + d / PlayerProperties.VELOCITY_STOP_DURATION, -1, 0)

        if not self.is_moving_up() and not self.is_moving_down():
            if -PlayerProperties.VELOCITY_THRESHOLD < self.velocity_y < PlayerProperties.VELOCITY_THRESHOLD and self.velocity_y != 0:
                self.velocity_y = 0
            if self.velocity_y > 0:
                self.velocity_y = clamp(self.velocity_y - d / PlayerProperties.VELOCITY_STOP_DURATION, 0, 1)
            elif self.velocity_y < 0:
                self.velocity_y = clamp(self.velocity_y + d / PlayerProperties.VELOCITY_STOP_DURATION, -1, 0)

        # Player - map boundaries collision
        if self._x < map_obj.get_x() or self._x > map_obj.get_x() + map_obj.get_width_in_pixels() - self.width:
            self._x = clamp(self._x, map_obj.get_x(), map_obj.get_x() + map_obj.get_width_in_pixels() - self.width)
            self.velocity_x = 0
        if self._y < map_obj.get_y() or self._y > map_obj.get_y() + map_obj.get_height_in_pixels() - self.height:
            self._y = clamp(self._y, map_obj.get_y(), map_obj.get_y() + map_obj.get_height_in_pixels() - self.height)
            self.velocity_y = 0

        # Player - wall collision
        if walls[0] and self._x <= tile_wx:
            self._x = tile_wx
            self.velocity_x = 0 if self.velocity_x < 0 else self.velocity_x
        if walls[1] and self._x >= tile_wx:
            self._x = tile_wx
            self.velocity_x = 0 if self.velocity_x > 0 else self.velocity_x
        if walls[2] and self._y <= tile_wy:
            self._y = tile_wy
            self.velocity_y = 0 if self.velocity_y < 0 else self.velocity_y
        if walls[3] and self._y >= tile_wy:
            self._y = tile_wy
            self.velocity_y = 0 if self.velocity_y > 0 else self.velocity_y
        if walls[4] and self._x + 1 < tile_wx and self._y + 1 < tile_wy:
            if abs(tile_wx - self._x) >= abs(tile_wy - self._y):
                self._y = tile_wy - 1
                self.velocity_y = 0 if self.velocity_y < 0 else self.velocity_y
            elif abs(tile_wx - self._x) < abs(tile_wy - self._y):
                self._x = tile_wx - 1
                self.velocity_x = 0 if self.velocity_x < 0 else self.velocity_x
        if walls[5] and self._x - 1 > tile_wx and self._y + 1 < tile_wy:
            if abs(tile_wx - self._x) >= abs(tile_wy - self._y):
                self._y = tile_wy - 1
                self.velocity_y = 0 if self.velocity_y < 0 else self.velocity_y
            elif abs(tile_wx - self._x) < abs(tile_wy - self._y):
                self._x = tile_wx + 1
                self.velocity_x = 0 if self.velocity_x > 0 else self.velocity_x
        if walls[6] and self._x + 1 < tile_wx and self._y - 1 > tile_wy:
            if abs(tile_wx - self._x) >= abs(tile_wy - self._y):
                self._y = tile_wy + 1
                self.velocity_y = 0 if self.velocity_y > 0 else self.velocity_y
            elif abs(tile_wx - self._x) < abs(tile_wy - self._y):
                self._x = tile_wx - 1
                self.velocity_x = 0 if self.velocity_x < 0 else self.velocity_x
        if walls[7] and self._x - 1 > tile_wx and self._y - 1 > tile_wy:
            if abs(tile_wx - self._x) >= abs(tile_wy - self._y):
                self._y = tile_wy + 1
                self.velocity_y = 0 if self.velocity_y > 0 else self.velocity_y
            elif abs(tile_wx - self._x) < abs(tile_wy - self._y):
                self._x = tile_wx + 1
                self.velocity_x = 0 if self.velocity_x > 0 else self.velocity_x

        # Prevent wall-clipping when lagging
        if self.is_in_wall(map_obj):
            self._x, self._y = prev_x, prev_y

        if self.breaking and self.can_break_breakable(map_obj) and not game.paused:
            self.break_tile(game)
        else:
            self.timers[Player.MINING_TIMER] = pygame.time.get_ticks() / 1000.0
            map_obj.tile_manager.draw(
                self.prev_selected_tile[0] * TileProperties.TILE_SIZE,
                self.prev_selected_tile[1] * TileProperties.TILE_SIZE,
                game.client.world.get_map().get_tile(self.prev_selected_tile[0], self.prev_selected_tile[1]),
                game.client.world.get_map().get_dynatile_surface()
            )

        # Update player health
        if self.is_in_lethal_tile(map_obj):
            tile_x, tile_y = game.client.world.get_map().get_tile_pos(self._x, self._y)
            tile = game.client.world.get_map().get_tile(tile_x, tile_y)
            if pygame.time.get_ticks() / 1000.0 - self.timers[Player.DAMAGE_TIMER] >= tile.get_damage_delay():
                self.health -= tile.get_damage()
                self.timers[Player.DAMAGE_TIMER] = pygame.time.get_ticks() / 1000.0
                self.hurt = True
            else:
                self.hurt = False

        # Game over
        if self.is_dead():
            self.health = 0
            game.screens.map_screen.set_state(False)

        self.main_hud.health_bar.set_value(self.health)

        self.edges[PlayerStates.MOVE_LEFT] = (self.screen_x <= game.width // 2 - self.width)
        self.edges[PlayerStates.MOVE_UP] = (self.screen_y <= game.height // 2 - self.height)
        self.edges[PlayerStates.MOVE_DOWN] = (self.screen_y >= game.height // 2 + self.height)
        self.edges[PlayerStates.MOVE_RIGHT] = (self.screen_x >= game.width // 2 + self.width)

    def update_ui(self) -> None:
        """
        Update the player GUI.
        """
        self.main_hud.update_ui()

    def break_tile(self, game) -> None:
        """
        Break a map tile and update map surfaces.
        """

        _map = game.client.world.get_map()
        tile_x, tile_y = self.selected_tile_x, self.selected_tile_y
        tile: Tile = _map.get_tile(self.selected_tile_x, self.selected_tile_y)
        delay: float = tile.get_resistance() / self.main_hud.hotbar.get_selected_slot_item().get_strength()

        if not 0 <= tile_x < _map.get_width_in_tiles() or not 0 <= tile_y < _map.get_height_in_tiles():
            return
        if _map.get_dynatile(tile_x, tile_y) or not _map.get_tile(tile_x, tile_y) in TileTypes.BREAKABLE:
            return

        if self.breaking_tile != (self.selected_tile_x, self.selected_tile_y):
            self.breaking_tile = (self.selected_tile_x, self.selected_tile_y)
            self.timers[Player.MINING_TIMER] = pygame.time.get_ticks() / 1000.0

        if self.prev_selected_tile != (self.selected_tile_x, self.selected_tile_y):
            _map.tile_manager.draw(
                self.prev_selected_tile[0] * TileProperties.TILE_SIZE,
                self.prev_selected_tile[1] * TileProperties.TILE_SIZE,
                _map.get_tile(self.prev_selected_tile[0], self.prev_selected_tile[1]),
                _map.get_dynatile_surface()
            )
            self.prev_selected_tile = (self.selected_tile_x, self.selected_tile_y)

        if pygame.time.get_ticks() / 1000.0 - self.timers[Player.MINING_TIMER] >= delay:
            _map.set_dynatile(tile_x, tile_y, True)
            _map.set_tile(tile_x, tile_y, Tiles.PLAINS)
            self.prev_broken_tile = (tile_x, tile_y)
            game.client.connection_handler.queue_packet(PlayerBuilder.get_compressed_player_packet(
                BaseBuilder.PLAYER_TILE_BREAK_COMMAND,
                self
            ))
            logger.debug(f'Destroyed tile ({tile_x}, {tile_y}) of type {tile}')
            return


        _map.tile_manager.draw(
            tile_x * TileProperties.TILE_SIZE,
            tile_y * TileProperties.TILE_SIZE,
            Tiles.BREAK_TILES_ANIM[
                int((pygame.time.get_ticks() / 1000.0
                     - self.timers[Player.MINING_TIMER])
                    / delay * (len(Tiles.BREAK_TILES_ANIM) - 1)
                )], _map.get_dynatile_surface()
        )

    def reset(self, map_obj: Map, camera_obj: Camera) -> None:
        """
        Reset the player's general attributes.
        """
        self._x = self._y = self.velocity_x = self.velocity_y = 0
        self.move = 0
        self.health = 100
        self.hurt = False
        self.set_ideal_spawn_point(map_obj, camera_obj)

    def is_moving_left(self) -> bool:
        """
        Return True if the player is moving left.
        """
        return bool((self.move >> PlayerStates.MOVE_LEFT) & 1)

    def is_moving_up(self) -> bool:
        """
        Return True if the player is moving up.
        """
        return bool((self.move >> PlayerStates.MOVE_UP) & 1)

    def is_moving_right(self) -> bool:
        """
        Return True if the player is moving right.
        """
        return bool((self.move >> PlayerStates.MOVE_RIGHT) & 1)

    def is_moving_down(self) -> bool:
        """
        Return True if the player is moving down.
        """
        return bool((self.move >> PlayerStates.MOVE_DOWN) & 1)

    def is_near_left_edge(self) -> bool:
        """
        Return True if the player is at the left-center of the screen.
        """
        return self.edges[PlayerStates.MOVE_LEFT]

    def is_near_top_edge(self) -> bool:
        """
        Return True if the player is at the top-center of the screen.
        """
        return self.edges[PlayerStates.MOVE_UP]

    def is_near_right_edge(self) -> bool:
        """
        Return True if the player is to the right-center of the screen.
        """
        return self.edges[PlayerStates.MOVE_RIGHT]

    def is_near_bottom_edge(self) -> bool:
        """
        Return True if the player is to the bottom-center of the screen.
        """
        return self.edges[PlayerStates.MOVE_DOWN]

    def is_in_water(self, map_obj: Map) -> bool:
        """
        Returns True if the player is in water.
        """
        tile_x, tile_y = map_obj.get_tile_pos(self._x, self._y)
        return map_obj.get_tile(tile_x, tile_y) == Tiles.WATER

    def is_in_lava(self, map_obj: Map) -> bool:
        """
        Returns True if the player is in lava.
        """
        tile_x, tile_y = map_obj.get_tile_pos(self._x, self._y)
        return map_obj.get_tile(tile_x, tile_y) == Tiles.LAVA

    def is_in_lethal_tile(self, map_obj: Map) -> bool:
        """
        Returns True if the player is touching a lethal tile.
        """
        tile_x, tile_y = map_obj.get_tile_pos(self._x, self._y)
        return map_obj.get_tile(tile_x, tile_y) in TileTypes.LETHAL

    def is_in_wall(self, map_obj: Map) -> bool:
        """
        Returns True if the player is surrounded by tiles with collision.
        """
        tile_x, tile_y = map_obj.get_tile_pos(self._x, self._y)
        return map_obj.get_tile(tile_x, tile_y) in TileTypes.BREAKABLE

    def get_held_item(self) -> bool:
        """
        Returns item held by player.
        """
        return self.main_hud.hotbar.get_selected_slot_item()

    def is_dead(self) -> bool:
        """
        Returns True if the player is dead.
        """
        return self.health <= 0

    def can_break_breakable(self, map_obj: Map) -> bool:
        """
        Returns True if the player is able to access and break a breakable tile.
        """
        return (pygame.mouse.get_pressed()[MouseStates.LMB - 1]
                and self.main_hud.hotbar.get_selected_slot_item() == Items.SHOVEL
                and self.has_selected_breakable(map_obj)
                and not self.is_selected_breakable_obstructed(map_obj))

    def has_selected_breakable(self, map_obj: Map) -> bool:
        """
        Returns True if the player has selected a breakable tile.
        """
        return map_obj.get_tile(self.selected_tile_x, self.selected_tile_y) in TileTypes.BREAKABLE

    def is_selected_breakable_obstructed(self, map_obj: Map) -> bool:
        """
        Returns True if the selected breakable tile is obstructed by other tiles with collision.
        """
        tile_x, tile_y = map_obj.get_tile_pos(self._x, self._y)
        x0, y0 = tile_x, tile_y
        x1, y1 = self.selected_tile_x, self.selected_tile_y

        # Bresenham (Thanks Wikipedia)
        dx = abs(x1 - x0)
        sx = 1 if x0 < x1 else -1
        dy = -abs(y1 - y0)
        sy = 1 if y0 < y1 else -1
        error = dx + dy

        while True:  # Nul à chier mais flm de corriger
            if not (x0 == x1 and y0 == y1) and map_obj.get_tile(x0, y0) in TileTypes.BREAKABLE:
                return True
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * error
            if e2 >= dy:
                if x0 == x1:
                    break
                error += dy
                x0 += sx
            if e2 <= dx:
                if y0 == y1:
                    break
                error += dx
                y0 += sy

        try:
            if (map_obj.get_tile(self.selected_tile_x - 1, self.selected_tile_y) in TileTypes.BREAKABLE
                    and map_obj.get_tile(self.selected_tile_x + 1, self.selected_tile_y) in TileTypes.BREAKABLE
                    and map_obj.get_tile(self.selected_tile_x, self.selected_tile_y - 1) in TileTypes.BREAKABLE
                    and map_obj.get_tile(self.selected_tile_x, self.selected_tile_y + 1) in TileTypes.BREAKABLE):
                return True
            if tile_x > self.selected_tile_x and tile_y > self.selected_tile_y:
                return (map_obj.get_tile(self.selected_tile_x + 1, self.selected_tile_y) in TileTypes.BREAKABLE
                        and map_obj.get_tile(self.selected_tile_x, self.selected_tile_y + 1) in TileTypes.BREAKABLE)
            if tile_x < self.selected_tile_x and tile_y > self.selected_tile_y:
                return (map_obj.get_tile(self.selected_tile_x - 1, self.selected_tile_y) in TileTypes.BREAKABLE
                        and map_obj.get_tile(self.selected_tile_x, self.selected_tile_y + 1) in TileTypes.BREAKABLE)
            if tile_x > self.selected_tile_x and tile_y < self.selected_tile_y:
                return (map_obj.get_tile(self.selected_tile_x + 1, self.selected_tile_y) in TileTypes.BREAKABLE
                        and map_obj.get_tile(self.selected_tile_x, self.selected_tile_y - 1) in TileTypes.BREAKABLE)
            if tile_x < self.selected_tile_x and tile_y < self.selected_tile_y:
                return (map_obj.get_tile(self.selected_tile_x - 1, self.selected_tile_y) in TileTypes.BREAKABLE
                        and map_obj.get_tile(self.selected_tile_x, self.selected_tile_y - 1) in TileTypes.BREAKABLE)
        except IndexError:
            return True
        return False

    def set_x(self, x: int) -> Self:
        """
        Set the player's x position, then return the player itself.
        """
        self._x = x
        return self

    def get_x(self) -> int:
        """
        Return the player's x position.
        """
        return self._x

    def set_y(self, y: int) -> Self:
        """
        Set the player's y position, then return the player itself.
        """
        self._y = y
        return self

    def get_y(self) -> int:
        """
        Return the player's y position.
        """
        return self._y

    def get_absolute_x(self, map_obj: Map) -> int:
        """
        Return the player's x position as if the map's top-left corner were to be positioned at the origin (0, 0).
        This signifies that the returned value will always be positive.
        """
        return self._x + map_obj.get_width_in_pixels() // 2

    def get_absolute_y(self, map_obj: Map) -> int:
        """
        Return the player's y position as if the map's top-left corner were to be positioned at the origin (0, 0).
        This signifies that the returned value will always be positive.
        """
        return self._y + map_obj.get_height_in_pixels() // 2

    def get_coefficient_from_center_x(self, parent_width: int) -> float:
        """
        Return the coefficient indicating how far the player is away from the horizontal center of the screen.
        """
        return 1 + abs(self.screen_x - parent_width // 2) / (parent_width // 2)

    def get_coefficient_from_center_y(self, parent_height: int) -> float:
        """
        Return the coefficient indicating how far the player is away from the vertical center of the screen.
        """
        return 1 + abs(self.screen_y - parent_height // 2) / (parent_height // 2)

    def get_selected_tile_x(self) -> int:
        """
        Return the selected tile's x position.
        """
        return self.selected_tile_x

    def get_selected_tile_y(self) -> int:
        """
        Return the selected tile's y position.
        """
        return self.selected_tile_y

    def set_health(self, health: int) -> Self:
        """
        Set the player's health, then return the player itself.
        """
        self.health = health
        return self

    def get_health(self) -> int:
        """
        Return the player's health.
        """
        return self.health

    def set_player_name(self, player_name: str):
        """
        Set the player's in-game name, then return the player itself.
        """
        self.player_name = player_name
        return self

    def get_player_name(self):
        """
        Return the player's in-game name.
        """
        return self.player_name

    def get_walls(self, map_obj: Map) -> list[bool]:
        """
        Return the tiles of type BREAKABLE surrounding the player.
        This is used for determining what tiles the player could potentially collide with.
        The order of the tiles are MOVE_LEFT, MOVE_RIGHT, MOVE_UP, MOVE_DOWN, UPPER MOVE_LEFT, UPPER MOVE_RIGHT, LOWER MOVE_LEFT, LOWER MOVE_RIGHT.
        """
        walls = [False] * 8
        tile_x, tile_y = map_obj.get_tile_pos(self._x, self._y)
        if tile_x > 0:
            walls[0] = map_obj.get_tile(tile_x - 1, tile_y) in TileTypes.BREAKABLE  # Left
        if tile_x < map_obj.get_width_in_tiles() - 1:
            walls[1] = map_obj.get_tile(tile_x + 1, tile_y) in TileTypes.BREAKABLE  # Right
        if tile_y > 0:
            walls[2] = map_obj.get_tile(tile_x, tile_y - 1) in TileTypes.BREAKABLE  # Up
        if tile_y < map_obj.get_height_in_tiles() - 1:
            walls[3] = map_obj.get_tile(tile_x, tile_y + 1) in TileTypes.BREAKABLE  # Down
        if tile_x > 0 and tile_y > 0:
            walls[4] = map_obj.get_tile(tile_x - 1, tile_y - 1) in TileTypes.BREAKABLE  # Upper left
        if tile_x < map_obj.get_width_in_tiles() - 1 and tile_y > 0:
            walls[5] = map_obj.get_tile(tile_x + 1, tile_y - 1) in TileTypes.BREAKABLE  # Upper right
        if tile_x > 0 and tile_y < map_obj.get_height_in_tiles() - 1:
            walls[6] = map_obj.get_tile(tile_x - 1, tile_y + 1) in TileTypes.BREAKABLE  # Lower left
        if tile_x < map_obj.get_width_in_tiles() - 1 and tile_y < map_obj.get_height_in_tiles() - 1:
            walls[7] = map_obj.get_tile(tile_x + 1, tile_y + 1) in TileTypes.BREAKABLE  # Lower right
        return walls

    def set_ideal_spawn_point(self, map_obj: Map, camera_obj: Camera, nb_attempts: int = 5) -> None:
        """
        Find the ideal starting position for the player when creating a new map.
        By default, five consecutive failed attempts will replace the tile at the last randomised tile position
        to plains and place the player there.
        Setting the number of attempts to anything less than 1 will raise an exception.
        """
        if nb_attempts < 1:
            raise ZeroOrLessSpawnPlayerAttempts

        tile_x: int = 0
        tile_y: int = 0
        bad_tiles = TileTypes.BREAKABLE + (Tiles.LAVA,)
        for i in range(nb_attempts):
            tile_x = randint(0, map_obj.get_width_in_tiles() - 1)
            tile_y = randint(0, map_obj.get_height_in_tiles() - 1)
            if map_obj.get_tile(tile_x, tile_y) not in bad_tiles:
                self._x, self._y = map_obj.tile_to_world_pos(tile_x, tile_y)
                camera_obj.x, camera_obj.y = self._x, self._y
                return
        map_obj.set_dynatile(tile_x, tile_y, True)
        map_obj.set_tile(tile_x, tile_y, Tiles.PLAINS)
        map_obj.tile_manager.draw(
            tile_x * TileProperties.TILE_SIZE,
            tile_y * TileProperties.TILE_SIZE,
            Tiles.PLAINS,
            map_obj.get_dynatile_surface()
        )
        self._x, self._y = map_obj.tile_to_world_pos(tile_x, tile_y)
        camera_obj.x, camera_obj.y = self._x, self._y

