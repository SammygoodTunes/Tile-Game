import math
from enum import Enum
import pygame
from pygame.math import clamp
from random import randint
from game.gui.label import Label
from game.gui.button import Button
from game.gui.hotbar import Hotbar
from game.gui.progress_bar import ProgressBar
from game.utils.tools import get_sign
from game.world.map_manager import Map
from game.data.tiles import Tiles, TileTypes
from game.data.items import Items
from game.data.mouse_properties import Mouse
from importlib import resources as impr
from game import assets


class Directions(Enum):
    DOWN, RIGHT, UP, LEFT = range(3, -1, -1)


class Player(pygame.sprite.Sprite):

    TEXTURE = impr.files(assets) / "player.png"
    DISTANCE_FROM_EDGE = 250
    VELOCITY_STEP_START = 4.5
    VELOCITY_STEP_STOP = 5

    TIMERS_COUNT = 2
    (
        MINING_TIMER,
        DAMAGE_TIMER
    ) = range(0, TIMERS_COUNT)

    def __init__(self, game, x=0, y=0, speed=50):
        super().__init__()
        self.game = game
        self.asset = pygame.image.load(Player.TEXTURE).convert_alpha(game.screen)
        self.x = x
        self.y = y
        self.screen_x = x
        self.screen_y = y
        self.width = 32
        self.height = 32
        self.velocity_x = 0
        self.velocity_y = 0
        self.speed = speed
        self.move = 0
        self.selected_tile_x = 0
        self.selected_tile_y = 0
        self.selected_tile_sx = 0
        self.selected_tile_sy = 0
        self.breaking_tile = None
        self.breaking = False
        self.hurt = False
        self.prev_selected_tile = (0, 0)
        self.score = 0
        self.health = 100
        self.score_label = (Label(f"Score: {self.score}", 4, -8)
                            .set_shadow_x(6).set_shadow_y(-6)
                            .set_colour((240, 240, 240)).set_shadow_colour((25, 25, 25)))
        self.camera_label = Label(f"Camera (XY): {round(self.game.camera.x)} {round(self.game.camera.y)}")
        self.position_label = Label(f"Player (XY): {round(self.x)} {round(self.y)}")
        self.regen_button = Button("Regenerate").set_state(True)
        self.health_bar = ProgressBar(title="Player health").set_value(self.health).set_state(True)
        self.hotbar = Hotbar(slot_count=6).select_slot(0)
        self.edges = [False, False, False, False]
        self.timers = [0] * Player.TIMERS_COUNT

    def events(self, e):
        if e.type == pygame.KEYDOWN:
            self.move |= (1 << Directions.LEFT.value) if e.key == pygame.K_q else self.move
            self.move |= (1 << Directions.UP.value) if e.key == pygame.K_z else self.move
            self.move |= (1 << Directions.RIGHT.value) if e.key == pygame.K_d else self.move
            self.move |= (1 << Directions.DOWN.value) if e.key == pygame.K_s else self.move
        elif e.type == pygame.KEYUP:
            self.move &= ~(1 << Directions.LEFT.value) if e.key == pygame.K_q else self.move
            self.move &= ~(1 << Directions.UP.value) if e.key == pygame.K_z else self.move
            self.move &= ~(1 << Directions.RIGHT.value) if e.key == pygame.K_d else self.move
            self.move &= ~(1 << Directions.DOWN.value) if e.key == pygame.K_s else self.move
        if e.type == pygame.MOUSEBUTTONDOWN:
            if self.regen_button.is_hovering_over() and not self.game.screens.loading_screen.get_state():
                self.game.world.get_map().regenerate()
                self.health = 100
            elif e.button == Mouse.LMB:
                self.breaking = True
                self.timers[Player.MINING_TIMER] = pygame.time.get_ticks() / 1000.0
                self.game.world.tile_manager.draw(
                    self.selected_tile_x * self.game.world.tile_manager.SIZE, 
                    self.selected_tile_y * self.game.world.tile_manager.SIZE,
                    self.game.world.get_map().get_tile(self.selected_tile_x, self.selected_tile_y), 
                    self.game.world.get_map().get_dynatile_surface()
                )
        elif e.type == pygame.MOUSEBUTTONUP:
            if e.button == Mouse.LMB:
                self.breaking = False
                self.timers[Player.MINING_TIMER] = pygame.time.get_ticks() / 1000.0
                self.game.world.tile_manager.draw(
                    self.selected_tile_x * self.game.world.tile_manager.SIZE, 
                    self.selected_tile_y * self.game.world.tile_manager.SIZE,
                    self.game.world.get_map().get_tile(self.selected_tile_x, self.selected_tile_y), 
                    self.game.world.get_map().get_dynatile_surface()
                )
            if e.button == Mouse.RMB:
                pass
        if e.type == pygame.MOUSEWHEEL:
            self.hotbar.unselect_slot(self.hotbar.get_selected_slot())
            self.hotbar.select_slot((self.hotbar.get_selected_slot() - e.y) % len(self.hotbar.get_slots()))
            self.hotbar.init_slots()

    def draw(self, screen):
        if not self.is_dead():
            self.screen_x = self.game.width / 2 - self.game.camera.x + self.x
            self.screen_y = self.game.height / 2 - self.game.camera.y + self.y
            if self.is_in_lava():
                pygame.draw.rect(screen, (220, 200, 200), (self.screen_x, self.screen_y, self.width, self.height))
                return
            if not self.is_in_water():
                pygame.draw.rect(screen, (255, 255, 255), (self.screen_x, self.screen_y, self.width, self.height))
                return
            pygame.draw.rect(screen, (200, 200, 220), (self.screen_x, self.screen_y, self.width, self.height))
        # screen.blit(self.asset, (self.screen_x, self.screen_y, self.width, self.height))

    def draw_ui(self, screen):
        if self.game.screens.options_screen.debug_info_box.is_checked():
            self.camera_label.set_text(f"Camera (XY): {round(self.game.camera.x)} {round(self.game.camera.y)}")
            self.position_label.set_text(f"Player (XY): {round(self.x)} {round(self.y)}")
            self.camera_label.draw(screen)
            self.position_label.draw(screen)
        self.score_label.set_text(f"Score: {self.score}")
        self.score_label.draw(screen)
        self.regen_button.set_state(not self.game.paused)
        self.regen_button.draw(screen)
        self.health_bar.draw(screen)
        self.hotbar.draw(screen)

    def draw_selection_grid(self, screen):
        if not self.game.paused and not self.is_dead() and self.hotbar.get_selected_slot_item() == Items.SHOVEL:
            mx, my = pygame.mouse.get_pos()
            
            center_x, center_y = self.game.width / 2, self.game.height / 2
            map_width, map_height = self.game.world.get_map().get_width_in_tiles(), self.game.world.get_map().get_height_in_tiles()
            camera_x, camera_y = round(self.game.camera.x), round(self.game.camera.y)

            wx, wy = (self.game.camera.x - (center_x - mx)) // 32, (self.game.camera.y - (center_y - my)) // 32
            wx, wy = clamp(wx, -map_width // 2, map_width // 2 - 1), clamp(wy, -map_height // 2, map_height // 2 - 1)

            x, y = self.game.world.get_map().tile_to_world_pos(wx + map_width // 2, wy + map_height // 2)
            self.selected_tile_sx, self.selected_tile_sy = x - camera_x + self.game.width // 2, y - camera_y + self.game.height // 2

            self.selected_tile_x = int(wx + map_width // 2)
            self.selected_tile_y = int(wy + map_height // 2)

            if self.has_selected_breakable() and not self.is_selected_breakable_obstructed():
                colour_anim: int = round(127.5 * math.sin(pygame.time.get_ticks() / 128) + 127.5)
                pygame.draw.rect(screen, (255, colour_anim, colour_anim), (
                                            self.selected_tile_sx, 
                                            self.selected_tile_sy, 
                                            self.game.world.tile_manager.SIZE, 
                                            self.game.world.tile_manager.SIZE
                                        ), 2, 4)

    def update(self, window, map_obj: Map):
        if not window.paused and not self.is_dead():
            d: float = window.clock.get_time() / 1000.0
            speed = (
                self.speed // (int(not self.is_in_water()) + 1.5 * self.is_in_water() + 1.5 * self.is_in_lava())
            )
            prev_x, prev_y = self.x, self.y

            if self.velocity_x != 0:
                self.x += speed * self.velocity_x * d
            if self.velocity_y != 0:
                self.y += speed * self.velocity_y * d

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
            if self.x < map_obj.get_x() or self.x > map_obj.get_x() + map_obj.get_width_in_pixels() - self.width or \
                    self.y < map_obj.get_y() or self.y > map_obj.get_y() + map_obj.get_height_in_pixels() - self.height:
                self.x = clamp(self.x, map_obj.get_x(), map_obj.get_x() + map_obj.get_width_in_pixels() - self.width)
                self.y = clamp(self.y, map_obj.get_y(), map_obj.get_y() + map_obj.get_height_in_pixels() - self.height)
                self.velocity_x = self.velocity_y = 0

            # Player - wall collision
            tile_x, tile_y = map_obj.get_tile_pos(self.x, self.y)
            tile_wx, tile_wy = map_obj.tile_to_world_pos(tile_x, tile_y)
            walls = self.get_walls()
            if walls[0] and self.x <= tile_wx:
                self.x = tile_wx
                self.velocity_x = 0 if self.velocity_x < 0 else self.velocity_x
            if walls[1] and self.x >= tile_wx:
                self.x = tile_wx
                self.velocity_x = 0 if self.velocity_x > 0 else self.velocity_x
            if walls[2] and self.y <= tile_wy:
                self.y = tile_wy
                self.velocity_y = 0 if self.velocity_y < 0 else self.velocity_y
            if walls[3] and self.y >= tile_wy:
                self.y = tile_wy
                self.velocity_y = 0 if self.velocity_y > 0 else self.velocity_y

            # Prevent wall-clipping when lagging
            if self.is_in_wall():
                self.x, self.y = prev_x, prev_y

            if self.breaking and self.can_break_breakable():
                self.break_tile()
            else:
                self.timers[Player.MINING_TIMER] = pygame.time.get_ticks() / 1000.0
                self.game.world.tile_manager.draw(
                    self.prev_selected_tile[0] * self.game.world.tile_manager.SIZE, 
                    self.prev_selected_tile[1] * self.game.world.tile_manager.SIZE,
                    self.game.world.get_map().get_tile(self.prev_selected_tile[0], self.prev_selected_tile[1]), 
                    self.game.world.get_map().get_dynatile_surface()
                )

            # Update player health
            if self.is_in_lethal_tile():
                tile_x, tile_y = self.game.world.get_map().get_tile_pos(self.x, self.y)
                tile = self.game.world.get_map().get_tile(tile_x, tile_y)
                if pygame.time.get_ticks() / 1000.0 - self.timers[Player.DAMAGE_TIMER] >= tile.get_damage_delay():
                    self.health -= tile.get_damage()
                    self.timers[Player.DAMAGE_TIMER] = pygame.time.get_ticks() / 1000.0
                    self.hurt = True
                else:
                    self.hurt = False

            # Game over
            if self.is_dead():
                self.health = 0
                self.game.screens.gameover_screen.set_state(True)

            self.health_bar.set_value(self.health)

            self.edges[Directions.LEFT.value] = (self.screen_x <= window.width // 2 - self.width // 2)
            self.edges[Directions.UP.value] = (self.screen_y <= window.height // 2 - self.height // 2)
            self.edges[Directions.DOWN.value] = (self.screen_y >= window.height // 2 + self.height // 2)
            self.edges[Directions.RIGHT.value] = (self.screen_x >= window.width // 2 + self.width // 2)

        else:
            self.move = 0


    def update_ui(self):
        y = -8
        self.regen_button.update(self.game)
        self.health_bar.update(self.game)
        self.hotbar.update(self.game)
        self.score_label.update(self.game)
        self.camera_label.update(self.game)
        self.position_label.update(self.game)
        self.regen_button.set_x(self.game.width - self.regen_button.get_width() - 4).set_y(40)
        self.health_bar.center_horizontally(0, self.game.width).set_y(self.health_bar.get_height())
        self.hotbar.set_y(self.game.height - self.hotbar.get_height() - 16).center_horizontally(0, self.game.width)
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

    def break_tile(self):
        tile_x, tile_y = self.selected_tile_x, self.selected_tile_y
        if not self.game.world.get_map().get_dynatile(tile_x, tile_y) and self.game.world.get_map().get_tile(tile_x, tile_y) in TileTypes.BREAKABLE.value:
            if self.breaking_tile != (self.selected_tile_x, self.selected_tile_y):
                self.breaking_tile = (self.selected_tile_x, self.selected_tile_y)
                self.timers[Player.MINING_TIMER] = pygame.time.get_ticks() / 1000.0
            
            if self.prev_selected_tile != (self.selected_tile_x, self.selected_tile_y):
                self.game.world.tile_manager.draw(
                    self.prev_selected_tile[0] * self.game.world.tile_manager.SIZE, 
                    self.prev_selected_tile[1] * self.game.world.tile_manager.SIZE,
                    self.game.world.get_map().get_tile(self.prev_selected_tile[0], self.prev_selected_tile[1]), 
                    self.game.world.get_map().get_dynatile_surface()
                )
                self.prev_selected_tile = (self.selected_tile_x, self.selected_tile_y)

            tile = self.game.world.get_map().get_tile(self.selected_tile_x, self.selected_tile_y)
            delay = tile.get_resistance() / self.hotbar.get_selected_slot_item().value.get_strength()

            if pygame.time.get_ticks() / 1000.0 - self.timers[Player.MINING_TIMER] >= delay:
                self.game.world.get_map().set_dynatile(tile_x, tile_y, True)
                self.game.world.get_map().set_tile(tile_x, tile_y, Tiles.PLAINS)
                self.game.world.tile_manager.draw(
                    tile_x * self.game.world.tile_manager.SIZE, 
                    tile_y * self.game.world.tile_manager.SIZE,
                    Tiles.PLAINS, 
                    self.game.world.get_map().get_dynatile_surface()
                )
            else:
                self.game.world.tile_manager.draw(
                    tile_x * self.game.world.tile_manager.SIZE, 
                    tile_y * self.game.world.tile_manager.SIZE,
                    self.game.world.get_map().get_tile(tile_x, tile_y), 
                    self.game.world.get_map().get_dynatile_surface()
                )
                self.game.world.tile_manager.draw(
                    tile_x * self.game.world.tile_manager.SIZE, 
                    tile_y * self.game.world.tile_manager.SIZE,
                    Tiles.BREAK_TILES_ANIM[int((pygame.time.get_ticks() / 1000.0 - self.timers[Player.MINING_TIMER]) / delay * (len(Tiles.BREAK_TILES_ANIM) - 1))], 
                    self.game.world.get_map().get_dynatile_surface()
                )


    def reset(self):
        self.x = self.y = self.velocity_x = self.velocity_y = 0
        self.move = 0
        self.health = 100
        self.hurt = False

    def is_moving_left(self) -> bool:
        return bool((self.move >> Directions.LEFT.value) & 1)

    def is_moving_up(self) -> bool:
        return bool((self.move >> Directions.UP.value) & 1)

    def is_moving_right(self) -> bool:
        return bool((self.move >> Directions.RIGHT.value) & 1)

    def is_moving_down(self) -> bool:
        return bool((self.move >> Directions.DOWN.value) & 1)

    def is_near_left_edge(self) -> bool:
        return self.edges[Directions.LEFT.value]

    def is_near_top_edge(self) -> bool:
        return self.edges[Directions.UP.value]

    def is_near_right_edge(self) -> bool:
        return self.edges[Directions.RIGHT.value]

    def is_near_bottom_edge(self) -> bool:
        return self.edges[Directions.DOWN.value]

    def is_in_water(self) -> bool:
        tile_x, tile_y = self.game.world.get_map().get_tile_pos(self.x, self.y)
        return self.game.world.get_map().get_tile(tile_x, tile_y) == Tiles.WATER

    def is_in_lava(self) -> bool:
        tile_x, tile_y = self.game.world.get_map().get_tile_pos(self.x, self.y)
        return self.game.world.get_map().get_tile(tile_x, tile_y) == Tiles.LAVA

    def is_in_lethal_tile(self) -> bool:
        tile_x, tile_y = self.game.world.get_map().get_tile_pos(self.x, self.y)
        return self.game.world.get_map().get_tile(tile_x, tile_y) in TileTypes.LETHAL.value

    def is_in_wall(self) -> bool:
        tile_x, tile_y = self.game.world.get_map().get_tile_pos(self.x, self.y)
        return self.game.world.get_map().get_tile(tile_x, tile_y) in TileTypes.BREAKABLE.value

    def is_dead(self) -> bool:
        return self.health <= 0

    def can_break_breakable(self) -> bool:
        return (pygame.mouse.get_pressed()[Mouse.LMB - 1] 
            and self.hotbar.get_selected_slot_item() == Items.SHOVEL
            and self.has_selected_breakable() 
            and not self.is_selected_breakable_obstructed())

    def has_selected_breakable(self) -> bool:
        return self.game.world.get_map().get_tile(self.selected_tile_x, self.selected_tile_y) in TileTypes.BREAKABLE.value

    def is_selected_breakable_obstructed(self) -> None:
        player_tile_x, player_tile_y = self.game.world.get_map().get_tile_pos(self.x, self.y)
        #tile_x = self.selected_tile_sx + 16
        #tile_y = self.selected_tile_sy + 16

        x0, y0, x1, y1 = player_tile_x, player_tile_y, self.selected_tile_x, self.selected_tile_y

        # Bresenham (Thanks Wikipedia)
        dx = abs(x1 - x0)
        sx = 1 if x0 < x1 else -1
        dy = -abs(y1 - y0)
        sy = 1 if y0 < y1 else -1
        error = dx + dy

        while True: # Nul à chier mais flm de corriger
            if not (x0 == x1 and y0 == y1) and self.game.world.get_map().get_tile(x0, y0) in TileTypes.BREAKABLE.value:
                return True
            # wx, wy = self.game.world.get_map().tile_to_screen_pos(x0, y0)
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
            if  (self.game.world.get_map().get_tile(self.selected_tile_x - 1, self.selected_tile_y) in TileTypes.BREAKABLE.value
                    and self.game.world.get_map().get_tile(self.selected_tile_x + 1, self.selected_tile_y) in TileTypes.BREAKABLE.value
                    and self.game.world.get_map().get_tile(self.selected_tile_x, self.selected_tile_y - 1) in TileTypes.BREAKABLE.value
                    and self.game.world.get_map().get_tile(self.selected_tile_x, self.selected_tile_y + 1) in TileTypes.BREAKABLE.value):
                return True
        except IndexError:
            return True
        # pygame.draw.line(screen, (255, 0, 0), (self.screen_x + 16, self.screen_y + 16), (tile_x, tile_y), 3)
        return False

    def set_x(self, x):
        self.x = x
        return self

    def get_x(self):
        return self.x

    def set_y(self, y):
        self.y = y
        return self

    def get_y(self):
        return self.y

    def get_coefficient_from_center_x(self):
        return 1 + abs(self.screen_x - self.game.width // 2) / (self.game.width // 2)

    def get_coefficient_from_center_y(self):
        return 1 + abs(self.screen_y - self.game.height // 2) / (self.game.height // 2)

    def get_selected_tile_x(self):
        return self.selected_tile_x

    def get_selected_tile_y(self):
        return self.selected_tile_y

    def set_health(self, health):
        self.health = health
        return self

    def get_health(self):
        return self.health

    def get_walls(self):
        walls = []
        try:
            tile_x, tile_y = self.game.world.get_map().get_tile_pos(self.x, self.y)
            walls.append(self.game.world.get_map().get_tile(tile_x - 1, tile_y) in TileTypes.BREAKABLE.value) # Left
            walls.append(self.game.world.get_map().get_tile(tile_x + 1, tile_y) in TileTypes.BREAKABLE.value) # Right
            walls.append(self.game.world.get_map().get_tile(tile_x, tile_y - 1) in TileTypes.BREAKABLE.value) # Up
            walls.append(self.game.world.get_map().get_tile(tile_x, tile_y + 1) in TileTypes.BREAKABLE.value) # Down
            walls.append(self.game.world.get_map().get_tile(tile_x - 1, tile_y - 1) in TileTypes.BREAKABLE.value) # Upper left
            walls.append(self.game.world.get_map().get_tile(tile_x + 1, tile_y - 1) in TileTypes.BREAKABLE.value) # Upper right
            walls.append(self.game.world.get_map().get_tile(tile_x - 1, tile_y + 1) in TileTypes.BREAKABLE.value) # Lower left
            walls.append(self.game.world.get_map().get_tile(tile_x + 1, tile_y + 1) in TileTypes.BREAKABLE.value) # Lower right
        except IndexError:
            for _ in range(4 - len(walls)):
                walls.append(False)
        return walls

    def set_ideal_spawnpoint(self):
        tile_x, tile_y = self.game.world.get_map().get_tile_pos(self.x, self.y)
        while self.game.world.get_map().get_tile(tile_x, tile_y) in TileTypes.BREAKABLE.value + [Tiles.LAVA]:
            tile_x, tile_y = self.game.world.get_map().get_tile_pos(self.x, self.y)
            tile_x = randint(0, self.game.world.get_map().get_width_in_tiles() - 1)
            tile_y = randint(0, self.game.world.get_map().get_height_in_tiles() - 1)
            self.x, self.y = self.game.world.get_map().tile_to_world_pos(tile_x, tile_y)
            self.game.camera.x, self.game.camera.y = self.x, self.y