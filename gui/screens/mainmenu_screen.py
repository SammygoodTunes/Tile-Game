
from .screen import Screen
from gui.label import Label
from gui.button import Button
import data.data_manager as data_mng


class MainMenu(Screen):

	def __init__(self, window):
		super().__init__()
		self.window = window
		self.title_label = Label(data_mng.get_game_property(data_mng.APP_NAME).strip()).set_font_sizes((15, 30, 50))
		self.play_button = Button("Play")
		self.set_state(True)

	def draw(self):
		if self._enabled:
			self.title_label.draw(self.window.screen)
			self.play_button.draw(self.window.screen)

	def update_ui(self):
		self.title_label.update(self.window)
		self.title_label.center_horizontally(0, self.window.width).set_y(100)
		self.play_button.update(self.window)
		self.play_button.center(0, 0, self.window.width, self.window.height)

	def set_state(self, state):
		super().set_state(state)
		self.title_label.set_state(state)
		self.play_button.set_state(state)
