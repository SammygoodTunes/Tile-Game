
from pygame import Surface

import game.data.data_manager as data_mng
from game.data.properties import ScreenProperties
from game.gui.screens.screen import Screen
from game.gui.label import Label
from game.gui.button import Button
from game.utils.logger import logger


class ServerMenuScreen(Screen):
	"""
	Class for creating the server menu screen.
	"""

	def __init__(self, window) -> None:
		super().__init__()
		self.window = window
		self.faded_surface = self.initialise_surface()
		self.subtitle_label = Label("Join a server or create one yourself for people to join.").set_font_sizes((7, 8, 10)).set_colour((215, 215, 215))
		self.join_button = Button("Join server").set_background_colour((150, 160, 255))
		self.join_button.label.set_colour((190, 200, 255))
		self.create_button = Button("Create server").set_background_colour((150, 255, 160))
		self.create_button.label.set_colour((190, 255, 200))
		self.back_button = Button("Back")
		logger.debug(f'Created {__class__.__name__} with attributes {self.__dict__}')

	def initialise_surface(self) -> Surface:
		"""
		Initialise the screen's surface.
		"""
		surface = Surface((self.window.width, self.window.height))
		surface.fill((0, 0, 0))
		surface.set_alpha(ScreenProperties.ALPHA)
		return surface

	def draw(self) -> None:
		"""
		Draw the screen and its components.
		"""
		if self._enabled:
			self.window.screen.blit(self.faded_surface, (0, 0))
			self.subtitle_label.draw(self.window.screen)
			self.join_button.draw(self.window.screen)
			self.create_button.draw(self.window.screen)
			self.back_button.draw(self.window.screen)

	def update_ui(self) -> None:
		"""
		Update the screen UI.
		"""
		self.faded_surface = self.initialise_surface()
		self.subtitle_label.update(self.window)
		self.subtitle_label.center_with_offset(0, 0, self.window.width, self.window.height, 0, -self.join_button.get_height() - self.subtitle_label.get_total_height() * 3)
		self.join_button.update(self.window)
		self.join_button.center_with_offset(0, 0, self.window.width, self.window.height, int(-self.create_button.get_width() // 1.5), -self.join_button.get_height())
		self.create_button.update(self.window)
		self.create_button.center_with_offset(0, 0, self.window.width, self.window.height, int(self.join_button.get_width() // 1.5), -self.join_button.get_height())
		self.back_button.update(self.window)
		self.back_button.center_with_offset(0, 0, self.window.width, self.window.height, 0, self.join_button.get_height() + self.create_button.get_height() + 10)

	def set_state(self, state: bool) -> None:
		"""
		Set the screen's visibility/interactivity.
		"""
		super().set_state(state)
		self.subtitle_label.set_state(state)
		self.join_button.set_state(state)
		self.create_button.set_state(state)
		self.back_button.set_state(state)
