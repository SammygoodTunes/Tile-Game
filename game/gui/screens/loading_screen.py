
from game.gui.screens.screen import Screen
from game.gui.progress_bar import ProgressBar
from game.gui.horizontal_slider import HorizontalSlider
from pygame import Surface, event, quit, QUIT, VIDEORESIZE


class LoadingScreen(Screen):

    def __init__(self, window):
        super().__init__()
        self.window = window
        self.surface = self.initialise_surface()
        self.progress_bar = ProgressBar()

    def initialise_surface(self):
        surface = Surface((self.window.width, self.window.height))
        surface.fill((0, 0, 0))
        return surface

    def events(self, e):
        pass

    def draw(self):
        if self._enabled:
            self.window.screen.blit(self.surface, (0, 0))
            self.progress_bar.draw(self.window.screen)

    def update_ui(self):
        self.surface = self.initialise_surface()
        self.progress_bar.update(self.window)
        self.progress_bar.center(0, 0, self.window.width, self.window.height)

    def set_state(self, state):
        super().set_state(state)
        self.progress_bar.set_state(state)
