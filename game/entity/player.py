from __future__ import annotations
import math
from importlib import resources as impr
import pygame
from pygame.math import clamp
from random import randint
from typing import Self

from game.data.items import Items
from game.data.mouse_properties import Mouse
from game.data.tiles import Tile, Tiles, TileTypes
from game.gui.button import Button
from game.gui.hotbar import Hotbar
from game.gui.label import Label
from game.gui.progress_bar import ProgressBar
from game.world.camera import Camera
from game.world.map_manager import Map


class Directions:
    """
    Class for defining the directions of the player.
    """

    LEFT: int
    RIGHT: int
    UP: int
    DOWN: int

    DOWN, RIGHT, UP, LEFT = range(3, -1, -1)


class Player:
    """
    Class for creating a player.
    """

    TEXTURE: str = str(impr.files("assets") / "player.png")
    VELOCITY_STEP_START: float = 4.5
    VELOCITY_STEP_STOP: float = 5.0

    TIMERS_COUNT: int = 2
    MINING_TIMER: int = 0
    DAMAGE_TIMER: int = 1

    def __init__(self, x: int = 0, y: int = 0, speed: int = 50) -> None:
        super().__init__()
        self.asset: pygame.Surface | None = None
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
        self.score: int = 0
        self.health: int = 100
        self.score_label: Label | None = None
        self.camera_label: Label | None = None
        self.position_label = Label(f"Player (XY): {self._x: .0f} {self._y: .0f}")
        self.regen_button = Button("Regenerate").set_state(True)
        self.health_bar = ProgressBar(title="Player health").set_value(self.health).set_state(True)
        self.hotbar = Hotbar(slot_count=6).select_slot(0)
        self.edges = [False, False, False, False]
        self.timers: list[float] = [0.0] * Player.TIMERS_COUNT

    def init(self, game: Game) -> None:
        """
        Define the player attributes that depend on the given game object.
        """
        self.asset = pygame.image.load(Player.TEXTURE).convert_alpha(game.screen)
        self.score_label = (Label(f"Score: {self.score}", 4, -8)
                            .set_shadow_x(6).set_shadow_y(-6)
                            .set_colour((240, 240, 240)).set_shadow_colour((25, 25, 25)))
        self.camera_label = Label(f"Camera (XY): {round(game.camera.x)} {round(game.camera.y)}")

    def events(self, game: Game, e: pygame.event.Event | pygame.event.EventType) -> None:
        """
        Track the player events.
        """
        if e.type == pygame.KEYDOWN:
            self.move |= (1 << Directions.LEFT) if e.key == pygame.K_q else self.move
            self.move |= (1 << Directions.UP) if e.key == pygame.K_z else self.move
            self.move |= (1 << Directions.RIGHT) if e.key == pygame.K_d else self.move
            self.move |= (1 << Directions.DOWN) if e.key == pygame.K_s else self.move
        elif e.type == pygame.KEYUP:
            self.move &= ~(1 << Directions.LEFT) if e.key == pygame.K_q else self.move
            self.move &= ~(1 << Directions.UP) if e.key == pygame.K_z else self.move
            self.move &= ~(1 << Directions.RIGHT) if e.key == pygame.K_d else self.move
            self.move &= ~(1 << Directions.DOWN) if e.key == pygame.K_s else self.move
        if e.type == pygame.MOUSEBUTTONDOWN:
            if self.regen_button.is_hovering_over() and not game.screens.loading_screen.get_state():
                game.world.get_map().regenerate(game)
                self.health = 100
            elif e.button == Mouse.LMB:
                self.breaking = True
                self.timers[Player.MINING_TIMER] = pygame.time.get_ticks() / 1000.0
                game.world.tile_manager.draw(
                    self.selected_tile_x * game.world.tile_manager.SIZE,
                    self.selected_tile_y * game.world.tile_manager.SIZE,
                    game.world.get_map().get_tile(self.selected_tile_x, self.selected_tile_y),
                    game.world.get_map().get_dynatile_surface()
                )
        elif e.type == pygame.MOUSEBUTTONUP:
            if e.button == Mouse.LMB:
                self.breaking = False
                self.timers[Player.MINING_TIMER] = pygame.time.get_ticks() / 1000.0
                game.world.tile_manager.draw(
                    self.selected_tile_x * game.world.tile_manager.SIZE,
                    self.selected_tile_y * game.world.tile_manager.SIZE,
                    game.world.get_map().get_tile(self.selected_tile_x, self.selected_tile_y),
                    game.world.get_map().get_dynatile_surface()
                )
            if e.button == Mouse.RMB:
                pass
        if e.type == pygame.MOUSEWHEEL:
            self.hotbar.unselect_slot(self.hotbar.get_selected_slot())
            self.hotbar.select_slot((self.hotbar.get_selected_slot() - e.y) % len(self.hotbar.get_slots()))
            self.hotbar.init_slots()

    def draw(self, game: Game) -> None:
        """
        Draw the player to the screen.
        """
        if not self.is_dead():
            self.screen_x = game.width / 2 - game.camera.x + self._x
            self.screen_y = game.height / 2 - game.camera.y + self._y
            if self.is_in_lava(game.world.get_map()):
                pygame.draw.rect(game.screen, (220, 200, 200), (self.screen_x, self.screen_y, self.width, self.height))
                return
            if not self.is_in_water(game.world.get_map()):
                pygame.draw.rect(game.screen, (255, 255, 255), (self.screen_x, self.screen_y, self.width, self.height))
                return
            pygame.draw.rect(game.screen, (200, 200, 220), (self.screen_x, self.screen_y, self.width, self.height))
        # screen.blit(self.asset, (self.screen_x, self.screen_y, self.width, self.height))

    def draw_ui(self, game: Game) -> None:
        """
        Draw the player GUI to the screen.
        """
        if game.screens.options_screen.debug_info_box.is_checked():
            self.camera_label.set_text(f"Camera (XY): {round(game.camera.x)} {round(game.camera.y)}")
            self.position_label.set_text(f"Player (XY): {round(self._x)} {round(self._y)}")
            self.camera_label.draw(game.screen)
            self.position_label.draw(game.screen)
        self.score_label.set_text(f"Score: {self.score}")
        self.score_label.draw(game.screen)
        self.regen_button.set_state(not game.paused)
        self.regen_button.draw(game.screen)
        self.health_bar.draw(game.screen)
        self.hotbar.draw(game.screen)

    def draw_selection_grid(self, game: Game) -> None:
        """
        Draw the player tile selection grid to the screen.
        """
        if not game.paused and not self.is_dead() and self.hotbar.get_selected_slot_item() == Items.SHOVEL:
            x: int
            y: int
            mx: int
            my: int
            wx: int
            wy: int
            center_x: int
            center_y: int
            map_width: int
            map_height: int

            mx, my = pygame.mouse.get_pos()
            center_x, center_y = round(game.width / 2), round(game.height / 2)
            map_width, map_height = game.world.get_map().get_width_in_tiles(), game.world.get_map().get_height_in_tiles()
            camera_x, camera_y = round(game.camera.x), round(game.camera.y)

            wx, wy = (game.camera.x - (center_x - mx)) // 32, (game.camera.y - (center_y - my)) // 32
            wx, wy = round(clamp(wx, -map_width // 2, map_width // 2 - 1)), round(clamp(wy, -map_height // 2, map_height // 2 - 1))

            x, y = game.world.get_map().tile_to_world_pos(wx + map_width // 2, wy + map_height // 2)
            self.selected_tile_sx, self.selected_tile_sy = x - camera_x + game.width // 2, y - camera_y + game.height // 2

            self.selected_tile_x = int(wx + map_width // 2)
            self.selected_tile_y = int(wy + map_height // 2)

            if self.has_selected_breakable(game.world.get_map()) and not self.is_selected_breakable_obstructed(game.world.get_map()):
                colour_anim: int = round(127.5 * math.sin(pygame.time.get_ticks() / 128) + 127.5)
                pygame.draw.rect(game.screen, (255, colour_anim, colour_anim), (
                                            self.selected_tile_sx,
                                            self.selected_tile_sy,
                                            game.world.tile_manager.SIZE,
                                            game.world.tile_manager.SIZE
                                        ), 2, 4)

    def update(self, game: Game, map_obj: Map) -> None:
        """
        Update the player.
        """
        if not game.paused and not self.is_dead():
            d: float = game.clock.get_time() / 1000.0
            prev_x: int = self._x
            prev_y: int = self._y
            speed: int = round(
                self.speed // (int(not self.is_in_water(map_obj))
                               + 1.5 * self.is_in_water(map_obj)
                               + 1.5 * self.is_in_lava(map_obj))
            )
            tile_x, tile_y = map_obj.get_tile_pos(self._x, self._y)
            tile_wx, tile_wy = map_obj.tile_to_world_pos(tile_x, tile_y)
            walls = self.get_walls(map_obj)

            if self.velocity_x != 0:
                self._x += speed * self.velocity_x * d
            if self.velocity_y != 0:
                self._y += speed * self.velocity_y * d

            if self.is_moving_left():
                self.velocity_x = clamp(self.velocity_x - Player.VELOCITY_STEP_START * d, -1, 1)
            if self.is_moving_right():
                self.velocity_x = clamp(self.velocity_x + Player.VELOCITY_STEP_START * d, -1, 1)
            if self.is_moving_up():
                self.velocity_y = clamp(self.velocity_y - Player.VELOCITY_STEP_START * d, -1, 1)
            if self.is_moving_down():
                self.velocity_y = clamp(self.velocity_y + Player.VELOCITY_STEP_START * d, -1, 1)

            if not self.is_moving_left() and not self.is_moving_right():
                if -0.0001 < self.velocity_x < 0.0001 and self.velocity_x != 0:
                    self.velocity_x = 0
                if self.velocity_x > 0:
                    self.velocity_x = clamp(self.velocity_x - Player.VELOCITY_STEP_STOP * d, 0, 1)
                elif self.velocity_x < 0:
                    self.velocity_x = clamp(self.velocity_x + Player.VELOCITY_STEP_STOP * d, -1, 0)

            if not self.is_moving_up() and not self.is_moving_down():
                if -0.0001 < self.velocity_y < 0.0001 and self.velocity_y != 0:
                    self.velocity_y = 0
                if self.velocity_y > 0:
                    self.velocity_y = clamp(self.velocity_y - Player.VELOCITY_STEP_STOP * d, 0, 1)
                elif self.velocity_y < 0:
                    self.velocity_y = clamp(self.velocity_y + Player.VELOCITY_STEP_STOP * d, -1, 0)

            # Player - map boundaries collision
            if self._x < map_obj.get_x() or self._x > map_obj.get_x() + map_obj.get_width_in_pixels() - self.width or \
                    self._y < map_obj.get_y() or self._y > map_obj.get_y() + map_obj.get_height_in_pixels() - self.height:
                self._x = clamp(self._x, map_obj.get_x(), map_obj.get_x() + map_obj.get_width_in_pixels() - self.width)
                self._y = clamp(self._y, map_obj.get_y(), map_obj.get_y() + map_obj.get_height_in_pixels() - self.height)
                self.velocity_x = self.velocity_y = 0

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

            # Prevent wall-clipping when lagging
            if self.is_in_wall(map_obj):
                self._x, self._y = prev_x, prev_y

            if self.breaking and self.can_break_breakable(map_obj):
                self.break_tile(game)
            else:
                self.timers[Player.MINING_TIMER] = pygame.time.get_ticks() / 1000.0
                game.world.tile_manager.draw(
                    self.prev_selected_tile[0] * game.world.tile_manager.SIZE,
                    self.prev_selected_tile[1] * game.world.tile_manager.SIZE,
                    game.world.get_map().get_tile(self.prev_selected_tile[0], self.prev_selected_tile[1]),
                    game.world.get_map().get_dynatile_surface()
                )

            # Update player health
            if self.is_in_lethal_tile(map_obj):
                tile_x, tile_y = game.world.get_map().get_tile_pos(self._x, self._y)
                tile = game.world.get_map().get_tile(tile_x, tile_y)
                if pygame.time.get_ticks() / 1000.0 - self.timers[Player.DAMAGE_TIMER] >= tile.get_damage_delay():
                    self.health -= tile.get_damage()
                    self.timers[Player.DAMAGE_TIMER] = pygame.time.get_ticks() / 1000.0
                    self.hurt = True
                else:
                    self.hurt = False

            # Game over
            if self.is_dead():
                self.health = 0
                game.screens.gameover_screen.set_state(True)

            self.health_bar.set_value(self.health)

            self.edges[Directions.LEFT] = (self.screen_x <= game.width // 2 - self.width // 2)
            self.edges[Directions.UP] = (self.screen_y <= game.height // 2 - self.height // 2)
            self.edges[Directions.DOWN] = (self.screen_y >= game.height // 2 + self.height // 2)
            self.edges[Directions.RIGHT] = (self.screen_x >= game.width // 2 + self.width // 2)

        else:
            self.move = 0

    def update_ui(self, game: Game) -> None:
        """
        Update the player GUI.
        """
        y: int = -8
        self.regen_button.update(game)
        self.health_bar.update(game)
        self.hotbar.update(game)
        self.score_label.update(game)
        self.camera_label.update(game)
        self.position_label.update(game)
        self.regen_button.set_x(game.width - self.regen_button.get_width() - 4).set_y(40)
        self.health_bar.center_horizontally(0, game.width).set_y(self.health_bar.get_height())
        self.hotbar.set_y(game.height - self.hotbar.get_height() - 16).center_horizontally(0, game.width)
        self.score_label.set_x(4)
        self.score_label.set_y(y)
        y += self.score_label.get_font_size() + 4
        self.camera_label.set_x(4)
        self.camera_label.set_y(y)
        y += self.camera_label.get_font_size() + 4
        self.position_label.set_x(4)
        self.position_label.set_y(y)
        self.regen_button.refresh()
        self.health_bar.refresh()
        self.score_label.refresh()
        self.position_label.refresh()

    def break_tile(self, game: Game) -> None:
        """
        Break a map tile and update map surfaces.
        """
        delay: float
        tile: Tile
        tile_x: int
        tile_y: int

        tile_x, tile_y = self.selected_tile_x, self.selected_tile_y
        if not game.world.get_map().get_dynatile(tile_x, tile_y) and game.world.get_map().get_tile(tile_x, tile_y) in TileTypes.BREAKABLE:
            if self.breaking_tile != (self.selected_tile_x, self.selected_tile_y):
                self.breaking_tile = (self.selected_tile_x, self.selected_tile_y)
                self.timers[Player.MINING_TIMER] = pygame.time.get_ticks() / 1000.0

            if self.prev_selected_tile != (self.selected_tile_x, self.selected_tile_y):
                game.world.tile_manager.draw(
                    self.prev_selected_tile[0] * game.world.tile_manager.SIZE,
                    self.prev_selected_tile[1] * game.world.tile_manager.SIZE,
                    game.world.get_map().get_tile(self.prev_selected_tile[0], self.prev_selected_tile[1]),
                    game.world.get_map().get_dynatile_surface()
                )
                self.prev_selected_tile = (self.selected_tile_x, self.selected_tile_y)

            tile = game.world.get_map().get_tile(self.selected_tile_x, self.selected_tile_y)
            delay = tile.get_resistance() / self.hotbar.get_selected_slot_item().get_strength()

            if pygame.time.get_ticks() / 1000.0 - self.timers[Player.MINING_TIMER] >= delay:
                game.world.get_map().set_dynatile(tile_x, tile_y, True)
                game.world.get_map().set_tile(tile_x, tile_y, Tiles.PLAINS)
                game.world.tile_manager.draw(
                    tile_x * game.world.tile_manager.SIZE,
                    tile_y * game.world.tile_manager.SIZE,
                    Tiles.PLAINS,
                    game.world.get_map().get_dynatile_surface()
                )
            else:
                game.world.tile_manager.draw(
                    tile_x * game.world.tile_manager.SIZE,
                    tile_y * game.world.tile_manager.SIZE,
                    game.world.get_map().get_tile(tile_x, tile_y),
                    game.world.get_map().get_dynatile_surface()
                )
                game.world.tile_manager.draw(
                    tile_x * game.world.tile_manager.SIZE,
                    tile_y * game.world.tile_manager.SIZE,
                    Tiles.BREAK_TILES_ANIM[int((pygame.time.get_ticks() / 1000.0 - self.timers[Player.MINING_TIMER]) / delay * (len(Tiles.BREAK_TILES_ANIM) - 1))],
                    game.world.get_map().get_dynatile_surface()
                )

    def reset(self) -> None:
        """
        Reset the player's general attributes.
        """
        self._x = self._y = self.velocity_x = self.velocity_y = 0
        self.move = 0
        self.health = 100
        self.hurt = False

    def is_moving_left(self) -> bool:
        """
        Return True if the player is moving left.
        """
        return bool((self.move >> Directions.LEFT) & 1)

    def is_moving_up(self) -> bool:
        """
        Return True if the player is moving up.
        """
        return bool((self.move >> Directions.UP) & 1)

    def is_moving_right(self) -> bool:
        """
        Return True if the player is moving right.
        """
        return bool((self.move >> Directions.RIGHT) & 1)

    def is_moving_down(self) -> bool:
        """
        Return True if the player is moving down.
        """
        return bool((self.move >> Directions.DOWN) & 1)

    def is_near_left_edge(self) -> bool:
        """
        Return True if the player is at the left-center of the screen.
        """
        return self.edges[Directions.LEFT]

    def is_near_top_edge(self) -> bool:
        """
        Return True if the player is at the top-center of the screen.
        """
        return self.edges[Directions.UP]

    def is_near_right_edge(self) -> bool:
        """
        Return True if the player is to the right-center of the screen.
        """
        return self.edges[Directions.RIGHT]

    def is_near_bottom_edge(self) -> bool:
        """
        Return True if the player is to the bottom-center of the screen.
        """
        return self.edges[Directions.DOWN]

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

    def is_dead(self) -> bool:
        """
        Returns True if the player is dead.
        """
        return self.health <= 0

    def can_break_breakable(self, map_obj: Map) -> bool:
        """
        Returns True if the player is able to access and break a breakable tile.
        """
        return (pygame.mouse.get_pressed()[Mouse.LMB - 1]
                and self.hotbar.get_selected_slot_item() == Items.SHOVEL
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
        x0, y0 = map_obj.get_tile_pos(self._x, self._y)
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
            # wx, wy = game.world.get_map().tile_to_screen_pos(x0, y0)
            # pygame.draw.rect(screen, (255, 255, 0), (wx, wy, 32, 32), 1, 3)
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
        except IndexError:
            return True
        # pygame.draw.line(screen, (255, 0, 0), (self.screen_x + 16, self.screen_y + 16), (tile_x, tile_y), 3)
        return False

    def set_x(self, x: int) -> Self:
        self._x = x
        return self

    def get_x(self) -> int:
        return self._x

    def set_y(self, y: int) -> Self:
        self._y = y
        return self

    def get_y(self) -> int:
        return self._y

    def get_coefficient_from_center_x(self, parent_width: int) -> float:
        return 1 + abs(self.screen_x - parent_width // 2) / (parent_width // 2)

    def get_coefficient_from_center_y(self, parent_height: int) -> float:
        return 1 + abs(self.screen_y - parent_height // 2) / (parent_height // 2)

    def get_selected_tile_x(self) -> int:
        return self.selected_tile_x

    def get_selected_tile_y(self) -> int:
        return self.selected_tile_y

    def set_health(self, health: int) -> Self:
        self.health = health
        return self

    def get_health(self) -> int:
        return self.health

    def get_walls(self, map_obj: Map) -> list[bool]:
        walls = []
        try:
            tile_x, tile_y = map_obj.get_tile_pos(self._x, self._y)
            walls.append(map_obj.get_tile(tile_x - 1, tile_y) in TileTypes.BREAKABLE)  # Left
            walls.append(map_obj.get_tile(tile_x + 1, tile_y) in TileTypes.BREAKABLE)  # Right
            walls.append(map_obj.get_tile(tile_x, tile_y - 1) in TileTypes.BREAKABLE)  # Up
            walls.append(map_obj.get_tile(tile_x, tile_y + 1) in TileTypes.BREAKABLE)  # Down
            walls.append(map_obj.get_tile(tile_x - 1, tile_y - 1) in TileTypes.BREAKABLE)  # Upper left
            walls.append(map_obj.get_tile(tile_x + 1, tile_y - 1) in TileTypes.BREAKABLE)  # Upper right
            walls.append(map_obj.get_tile(tile_x - 1, tile_y + 1) in TileTypes.BREAKABLE)  # Lower left
            walls.append(map_obj.get_tile(tile_x + 1, tile_y + 1) in TileTypes.BREAKABLE)  # Lower right
        except IndexError:
            for _ in range(4 - len(walls)):
                walls.append(False)
        return walls

    def set_ideal_spawnpoint(self, map_obj: Map, camera_obj: Camera) -> None:
        tile_x, tile_y = map_obj.get_tile_pos(self._x, self._y)
        while map_obj.get_tile(tile_x, tile_y) in TileTypes.BREAKABLE + (Tiles.LAVA,):
            tile_x, tile_y = map_obj.get_tile_pos(self._x, self._y)
            tx = randint(0, map_obj.get_width_in_tiles() - 1)
            ty = randint(0, map_obj.get_height_in_tiles() - 1)
            self._x, self._y = map_obj.tile_to_world_pos(tx, ty)
            camera_obj.x, camera_obj.y = self._x, self._y
