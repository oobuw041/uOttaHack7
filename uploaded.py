from colours import *
from config import *


class Uploaded:
    def __init__(self, main):
        self.graphics = main.graphics
        self.events = main.events
        self.win = main.win
        self.main = main

    def start(self, args=None):
        self.scale()

    def scale(self):
        pass

    def end(self):
        pass

    def update(self, dt):
        if self.events.resize:
            self.scale()

    def draw(self):
        self.win.fill(RED)
