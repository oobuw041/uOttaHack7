from colours import *
from config import *

class App:
    def __init__(self, main):
        self.graphics = main.graphics
        self.events = main.events
        self.win = main.win
        self.main = main

    def start(self, args=None):
        pass

    def end(self):
        pass

    def update(self, dt):
        pass

    def draw(self):
        self.win.fill(RED)
