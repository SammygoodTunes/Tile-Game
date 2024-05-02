
from pygame import Surface
from pygame.event import Event

import game.data.data_manager as data_mng
from game.gui.screens.screen import Screen
from game.gui.label import Label
from game.gui.button import Button
from game.gui.inputbox import InputBox
from game.utils.logger import logger


class ServerJoinScreen(Screen):
	"""
	Class for creating the server join screen.
	"""

	def __init__(self, window) -> None:
		super().__init__()
		self.window = window
		self.faded_surface = self.initialise_surface()
		self.subtitle_label = Label("Type the IP address and port of the server to join.").set_font_sizes((7, 8, 10)).set_colour((215, 215, 215))
		self.ip_input = InputBox(placeholder="Server IP").set_max_text_length(32)
		self.port_input = InputBox(placeholder="Port").set_max_text_length(5).authorise_only_numeric()
		self.join_button = Button("Join")
		self.back_button = Button("Back")
		logger.debug(f'Created {__class__.__name__} with attributes {self.__dict__}')

	def initialise_surface(self) -> Surface:
		"""
		Initialise the screen's surface.
		"""
		surface = Surface((self.window.width, self.window.height))
		surface.fill((0, 0, 0))
		surface.set_alpha(96)
		return surface

	def events(self, e: Event) -> None:
		"""
		Track the screen events (unused).
		"""
		self.ip_input.events(e)
		self.port_input.events(e)
		self.join_button.set_state(self.ip_input.get_text().strip() and self.port_input.get_text().strip())

	def draw(self) -> None:
		"""
		Draw the screen and its components.
		"""
		if self._enabled:
			self.window.screen.blit(self.faded_surface, (0, 0))
			self.subtitle_label.draw(self.window.screen)
			self.ip_input.draw(self.window.screen)
			self.port_input.draw(self.window.screen)
			self.join_button.draw(self.window.screen)
			self.back_button.draw(self.window.screen)

	def update_ui(self) -> None:
		"""
		Update the screen UI.
		"""
		self.faded_surface = self.initialise_surface()
		self.subtitle_label.update(self.window)
		self.subtitle_label.center_with_offset(0, 0, self.window.width, self.window.height, 0, -self.ip_input.get_height() - self.subtitle_label.get_total_height() * 3)
		self.ip_input.update(self.window)
		self.ip_input.center_with_offset(0, 0, self.window.width, self.window.height, 0, -self.ip_input.get_height())
		self.port_input.update(self.window)
		self.port_input.center_with_offset(0, 0, self.window.width, self.window.height, 0, 5)
		self.join_button.update(self.window)
		self.join_button.center_with_offset(0, 0, self.window.width, self.window.height, 0, self.ip_input.get_height() + self.port_input.get_height() + 10)
		self.back_button.update(self.window)
		self.back_button.center_with_offset(0, 0, self.window.width, self.window.height, 0, self.ip_input.get_height() + self.port_input.get_height() + self.join_button.get_height() + 15)

	def set_state(self, state: bool) -> None:
		"""
		Set the screen's visibility/interactivity.
		"""
		super().set_state(state)
		self.subtitle_label.set_state(state)
		self.ip_input.set_state(state)
		self.port_input.set_state(state)
		self.join_button.set_state(state)
		self.back_button.set_state(state)
