
from game.gui.screens.screen import Screen
from game.gui.label import Label
from game.gui.button import Button
import game.data.data_manager as data_mng
from game.utils.logger import logger


class MainMenu(Screen):

	def __init__(self, window):
		super().__init__()
		self.window = window
		self.title_label = Label(data_mng.get_game_property(data_mng.APP_NAME).strip()).set_font_sizes((15, 30, 50)).set_colour((200, 200, 255))
		self.play_button = Button("Play")
		self.options_button = Button("Options")
		self.credits_button = Button("Credits")
		self.quit_button = Button("Quit")
		self.set_state(True)
		logger.debug(f'Created {__class__.__name__} with attributes {self.__dict__}')

	def draw(self):
		if self._enabled:
			self.title_label.draw(self.window.screen)
			self.play_button.draw(self.window.screen)
			self.options_button.draw(self.window.screen)
			self.credits_button.draw(self.window.screen)
			self.quit_button.draw(self.window.screen)

	def update_ui(self):
		self.title_label.update(self.window)
		self.title_label.center_with_offset(0, 0, self.window.width, self.window.height, 0, -self.title_label.get_total_height())
		self.play_button.update(self.window)
		self.play_button.center(0, 0, self.window.width, self.window.height)
		self.options_button.update(self.window)
		self.options_button.center_with_offset(0, 0, self.window.width, self.window.height, 0, self.play_button.get_height() + 5)
		self.credits_button.update(self.window)
		self.credits_button.center_with_offset(0, 0, self.window.width, self.window.height, 0, self.play_button.get_height() + self.options_button.get_height() + 10)
		self.quit_button.update(self.window)
		self.quit_button.center_with_offset(0, 0, self.window.width, self.window.height, 0, self.play_button.get_height() + self.options_button.get_height() + self.credits_button.get_height() + 15)

	def set_state(self, state):
		super().set_state(state)
		self.title_label.set_state(state)
		self.play_button.set_state(state)
		self.options_button.set_state(state)
		self.credits_button.set_state(state)
		self.quit_button.set_state(state)
