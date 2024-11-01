"""
Module name: screen_manager

This module manages all the GUIs, their visibility and their behaviour.
"""

import pygame

from game.data.keys import Keys
from game.data.properties.game_properties import GameProperties
from game.data.states.connection_states import ConnectionStates
from game.data.states.mouse_states import MouseStates
from game.data.states.server_states import ServerStates
from game.gui.screens.crash_screen import CrashScreen
from game.gui.screens.credits_screen import CreditsScreen
from game.gui.screens.gameover_screen import GameoverScreen
from game.gui.screens.loading_screen import LoadingScreen
from game.gui.screens.mainmenu_screen import MainMenuScreen
from game.gui.screens.map_screen import MapScreen
from game.gui.screens.options_screen import OptionsScreen
from game.gui.screens.pause_screen import PauseScreen
from game.gui.screens.playerlist_screen import PlayerListScreen
from game.gui.screens.serverconnect_screen import ServerConnectScreen
from game.gui.screens.servercreate_screen import ServerCreateScreen
from game.gui.screens.serverjoin_screen import ServerJoinScreen
from game.gui.screens.servermenu_screen import ServerMenuScreen
from game.world.theme_manager import ThemeManager


class Screens:
    """
    Class for creating a collection of screens.
    """

    def __init__(self, game) -> None:
        self.game = game
        self.crash_screen = CrashScreen(game)
        self.credits_screen = CreditsScreen(game)
        self.gameover_screen = GameoverScreen(game)
        self.loading_screen = LoadingScreen(game)
        self.main_menu_screen = MainMenuScreen(game)
        self.map_screen = MapScreen(game)
        self.options_screen = OptionsScreen(game)
        self.pause_screen = PauseScreen(game)
        self.player_list_screen = PlayerListScreen(game)
        self.server_connect_screen = ServerConnectScreen(game)
        self.server_create_screen = ServerCreateScreen(game)
        self.server_join_screen = ServerJoinScreen(game)
        self.server_menu_screen = ServerMenuScreen(game)

    def events(self, e: pygame.event.Event) -> None:
        """
        Handle the events of the different screens.
        """
        if self.game.start_game:
            self.map_screen.initialise_map()

        self.server_join_screen.events(e)
        self.server_create_screen.events(e)
        self.options_screen.events(e)

        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE and self.game.start_game and not self.server_connect_screen.get_state() and not self.gameover_screen.get_state():
                if self.options_screen.get_state():
                    self.options_screen.set_state(not self.options_screen.get_state())
                else:
                    self.pause_screen.set_state(not self.pause_screen.get_state())
                    self.map_screen.set_state(False)
                    self.player_list_screen.set_state(False)
                self.game.paused = self.pause_screen.get_state()
            if e.key == pygame.K_ESCAPE and not self.server_connect_screen.get_state() and not self.main_menu_screen.get_state() and not self.game.start_game:
                self.server_menu_screen.set_state(False)
                self.server_create_screen.set_state(False)
                self.server_join_screen.set_state(False)
                self.options_screen.set_state(False)
                self.credits_screen.set_state(False)
                self.main_menu_screen.set_state(True)
            if e.key == pygame.K_ESCAPE and self.server_connect_screen.get_state() and self.server_connect_screen.main_menu_button.get_state():
                self.server_connect_screen.set_state(False)
                self.main_menu_screen.set_state(True)

            if e.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                if self.server_create_screen.get_state() and self.server_create_screen.create_button.get_state():
                    self.task_create_server()
                if self.server_join_screen.get_state() and self.server_join_screen.join_button.get_state():
                    self.task_join_server()

            if e.key == Keys.SHOW_MAP and self.game.start_game and not self.game.client.player.is_dead() and not self.game.paused:
                self.map_screen.set_state(True)
            if e.key == Keys.SHOW_PLAYERLIST and self.game.start_game and not self.game.client.player.is_dead() and not self.game.paused:
                self.player_list_screen.set_state(True)

        if e.type == pygame.KEYUP:
            if e.key == Keys.SHOW_MAP and self.game.start_game and not self.game.client.player.is_dead() and not self.game.paused:
                self.map_screen.set_state(False)
            if e.key == Keys.SHOW_PLAYERLIST and self.game.start_game and not self.game.client.player.is_dead() and not self.game.paused:
                self.player_list_screen.set_state(False)

        if e.type == pygame.MOUSEBUTTONUP:
            if e.button != MouseStates.LMB:
                return
        else:
            return

        if self.main_menu_screen.play_button.is_hovering_over() and self.main_menu_screen.get_state():
            self.main_menu_screen.set_state(False)
            self.server_menu_screen.set_state(True)
        elif self.main_menu_screen.options_button.is_hovering_over() and self.main_menu_screen.get_state():
            self.options_screen.set_state(True)
            self.main_menu_screen.set_state(False)
        elif self.main_menu_screen.credits_button.is_hovering_over() and self.main_menu_screen.get_state():
            self.credits_screen.set_state(True)
            self.main_menu_screen.set_state(False)
        elif self.main_menu_screen.quit_button.is_hovering_over() and self.main_menu_screen.get_state():
            self.game.stop()

        elif self.options_screen.back_button.is_hovering_over() and self.options_screen.get_state():
            self.options_screen.set_state(False)
            if self.game.start_game:
                self.pause_screen.set_state(True)
                return None
            self.main_menu_screen.set_state(True)
        elif self.credits_screen.back_button.is_hovering_over() and self.credits_screen.get_state():
            self.credits_screen.set_state(False)
            self.main_menu_screen.set_state(True)

        elif self.server_menu_screen.join_button.is_hovering_over() and self.server_menu_screen.get_state():
            self.server_menu_screen.set_state(False)
            self.server_join_screen.set_state(True)
            pygame.key.set_repeat(GameProperties.KEY_DELAY, GameProperties.KEY_INTERVAL)
            self.server_join_screen.join_button.set_state(
                self.server_join_screen.ign_input.get_text().strip()
                and self.server_join_screen.ip_input.get_text().strip()
                and self.server_join_screen.port_input.get_text().strip()
            )
            self.server_join_screen.ign_input.set_text(self.game.client.player.get_player_name())
            self.server_join_screen.update_ui()
        elif self.server_menu_screen.create_button.is_hovering_over() and self.server_menu_screen.get_state():
            self.server_menu_screen.set_state(False)
            self.server_create_screen.set_state(True)
            pygame.key.set_repeat(GameProperties.KEY_DELAY, GameProperties.KEY_INTERVAL)
            self.server_create_screen.create_button.set_state(
                bool(self.server_create_screen.ign_input.get_text().strip())
            )
            self.server_create_screen.ign_input.set_text(self.game.client.player.get_player_name())
            self.server_create_screen.update_ui()

        elif self.server_menu_screen.back_button.is_hovering_over() and self.server_menu_screen.get_state():
            self.server_menu_screen.set_state(False)
            self.main_menu_screen.set_state(True)

        elif self.server_join_screen.join_button.is_hovering_over() and self.server_join_screen.get_state():
            self.task_join_server()
        elif self.server_join_screen.back_button.is_hovering_over() and self.server_join_screen.get_state():
            self.server_join_screen.set_state(False)
            self.server_menu_screen.set_state(True)
            pygame.key.set_repeat()

        elif self.server_create_screen.create_button.is_hovering_over() and self.server_create_screen.get_state():
            self.task_create_server()
        elif self.server_create_screen.back_button.is_hovering_over() and self.server_create_screen.get_state():
            self.server_create_screen.set_state(False)
            self.server_menu_screen.set_state(True)
            pygame.key.set_repeat()

        elif self.server_connect_screen.main_menu_button.is_hovering_over() and self.server_connect_screen.get_state():
            self.server_connect_screen.set_state(False)
            self.server_connect_screen.reset_info_label()
            self.main_menu_screen.set_state(True)

        elif self.pause_screen.resume_button.is_hovering_over() and self.pause_screen.get_state():
            self.pause_screen.set_state(False)
            self.game.paused = False
        elif self.pause_screen.options_button.is_hovering_over() and self.pause_screen.get_state():
            self.pause_screen.set_state(False)
            self.options_screen.set_state(True)
        elif self.pause_screen.disconnect_button.is_hovering_over() and self.pause_screen.get_state():
            self.game.start_game = False
            self.game.paused = False
            self.game.client.connection_handler.stop_connection = True
            self.pause_screen.set_state(False)
            self.main_menu_screen.set_state(True)
            self.map_screen.reset_map()
            self.game.client.player.reset()
            self.game.client.player.set_ideal_spawn_point(self.game.client.world.get_map(), self.game.client.camera)

        elif self.gameover_screen.respawn_button.is_hovering_over() and self.gameover_screen.get_state():
            self.gameover_screen.set_state(False)
            self.game.client.player.reset()
            self.game.client.player.set_ideal_spawn_point(self.game.client.world.get_map(), self.game.client.camera)
        elif self.gameover_screen.disconnect_button.is_hovering_over() and self.gameover_screen.get_state():
            self.game.start_game = False
            self.game.paused = False
            self.game.client.connection_handler.stop_connection = True
            self.gameover_screen.set_state(False)
            self.main_menu_screen.set_state(True)
            self.map_screen.set_state(False)
            self.player_list_screen.set_state(False)
            self.game.client.player.reset()
            self.game.client.player.set_ideal_spawn_point(self.game.client.world.get_map(), self.game.client.camera)

    def update(self) -> None:
        """
        Update the screens.
        """
        self.crash_screen.draw()
        self.main_menu_screen.draw()
        self.server_menu_screen.draw()
        self.server_join_screen.draw()
        self.server_create_screen.draw()
        self.server_connect_screen.draw()
        self.loading_screen.draw()
        self.pause_screen.draw()
        self.options_screen.draw()
        self.credits_screen.draw()
        self.gameover_screen.draw()
        self.map_screen.draw()
        self.player_list_screen.draw()

    def update_ui(self) -> None:
        """
        Update the screen UIs.
        """
        self.crash_screen.update_ui()
        self.main_menu_screen.update_ui()
        self.server_menu_screen.update_ui()
        self.server_join_screen.update_ui()
        self.server_create_screen.update_ui()
        self.server_connect_screen.update_ui()
        self.loading_screen.update_ui()
        self.pause_screen.update_ui()
        self.options_screen.update_ui()
        self.credits_screen.update_ui()
        self.gameover_screen.update_ui()
        self.map_screen.update_ui()
        self.player_list_screen.update_ui()

    def task_create_server(self) -> None:
        """
        Screen task for creating a server.
        """
        pygame.key.set_repeat()
        self.server_create_screen.set_state(False)
        self.server_connect_screen.set_state(True)
        self.server_connect_screen.main_menu_button.set_state(False)
        self.game.client.player.set_player_name(self.server_create_screen.ign_input.get_text().strip())
        self.game.server.start(
            self.server_create_screen.seed_input.get_text().strip(),
            ThemeManager.get_theme_by_id(self.server_create_screen.world_theme_select.get_current_index()),
            self.server_create_screen.world_size_select.get_selected()
        )
        if self.game.server.state.value != ServerStates.FAIL:
            self.game.client.connection_handler.host = 'localhost'
            self.game.client.connection_handler.port = 35000
            self.game.client.connection_handler.player_name = self.server_create_screen.ign_input.get_text().strip()
            self.game.client.connection_handler.start_connection = True
        else:
            self.server_connect_screen.main_menu_button.set_state(True)
            self.server_connect_screen.update_info_label(ConnectionStates.SERVFAIL)

    def task_join_server(self) -> None:
        """
        Screen task for joining a server.
        """
        pygame.key.set_repeat()
        self.server_join_screen.set_state(False)
        self.server_connect_screen.set_state(True)
        self.server_connect_screen.main_menu_button.set_state(False)
        self.game.client.player.set_player_name(self.server_join_screen.ign_input.get_text().strip())
        self.game.client.connection_handler.player_name = self.server_join_screen.ign_input.get_text().strip()
        self.game.client.connection_handler.start_connection = True
