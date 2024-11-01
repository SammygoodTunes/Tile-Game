"""
Module name: servermenu_screen
"""

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING: from game.core.game import Game
from game.gui.screens.screen import Screen
from game.gui.label import Label
from game.gui.button import Button


class ServerMenuScreen(Screen):
	"""
	Class for creating the server menu screen.
	"""

	def __init__(self, game: Game) -> None:
		super().__init__(game)
		self.faded_surface = self.initialise_surface()
		self.subtitle_label = Label("Join a server or create one yourself for people to join.").set_font_sizes((7, 8, 10)).set_colour((215, 215, 215))
		self.join_button = Button("Join server").set_background_colour((150, 160, 255))
		self.join_button.label.set_colour((190, 200, 255))
		self.create_button = Button("Create server").set_background_colour((150, 255, 160))
		self.create_button.label.set_colour((190, 255, 200))
		self.back_button = Button("Back")

	def draw(self) -> None:
		if not self._enabled: return
		self.game.screen.blit(self.faded_surface, (0, 0))
		self.subtitle_label.draw(self.game.screen)
		self.join_button.draw(self.game.screen)
		self.create_button.draw(self.game.screen)
		self.back_button.draw(self.game.screen)

	def update_ui(self) -> None:
		if not self._enabled: return
		self.faded_surface = self.initialise_surface()
		self.join_button.resize(self.game)
		self.create_button.resize(self.game)
		self.back_button.resize(self.game)
		self.subtitle_label.update(self.game)
		self.subtitle_label.center_with_offset(
			0,
			0,
			self.game.width,
			self.game.height,
			0,
			-self.join_button.get_height() - self.subtitle_label.get_height() * 3
		)
		self.join_button.center_with_offset(
			0,
			0,
			self.game.width,
			self.game.height,
			int(-self.join_button.get_width() // 1.5),
			-self.join_button.get_height()
		)
		self.create_button.center_with_offset(
			0,
			0,
			self.game.width,
			self.game.height,
			int(self.create_button.get_width() // 1.5),
			-self.join_button.get_height()
		)
		self.back_button.center_with_offset(
			0,
			0,
			self.game.width,
			self.game.height,
			0,
			self.join_button.get_height() + self.create_button.get_height() + 10
		)
		self.join_button.update(self.game)
		self.create_button.update(self.game)
		self.back_button.update(self.game)

	def set_state(self, state: bool) -> None:
		super().set_state(state)
		self.subtitle_label.set_state(state)
		self.join_button.set_state(state)
		self.create_button.set_state(state)
		self.back_button.set_state(state)
		if state: self.update_ui()
