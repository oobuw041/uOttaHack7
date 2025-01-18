import pygame
import sys
from config import *
from colours import *
from graphics import Graphics
from events import Events
from app import App


class Main:
    def __init__(self, locations=None):
        pygame.init()

        self.win = pygame.display.set_mode(
            pygame.display.get_desktop_sizes()[0] if (RESX, RESY) == (0, 0) else (RESX, RESY),
            pygame.FULLSCREEN * FULLSCREEN | pygame.NOFRAME * BORDERLESS | pygame.RESIZABLE * RESIZABLE)
        pygame.display.set_caption(NAME)

        # remove after
        try:
            pygame.display.set_icon(pygame.image.load("assets\\icon.png"))
        except FileNotFoundError:
            pass

        self.clock = pygame.time.Clock()

        self.graphics = Graphics(self.win)
        self.events = Events()

        self.graphics.load_folder("assets")

        self.locations = {"app": App(self)}
        if locations is not None:
            for key, item in locations.items():
                self.locations[key] = item(self)
        self.location = None

    def set_location(self, loc, args=None):
        if self.location is not None:
            self.locations[self.location].end()
        self.location = loc
        self.locations[self.location].start(args)

    def close(self):
        self.locations[self.location].end()
        pygame.quit()
        sys.exit()

    def run(self, location="default"):
        self.set_location(location)

        clk = pygame.time.Clock()

        while True:
            self.events.update()
            dt = clk.tick(FPS)

            loc = self.locations[self.location]
            loc.update(dt)

            if self.events.quit:
                self.close()

            loc.draw()

            pygame.display.update()


Main().run("app")
