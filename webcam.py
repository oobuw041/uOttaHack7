from threading import Thread

import cv2

import translator
from colours import *
import pyvidplayer2
from config import *


class Webcam:
    def __init__(self, main):
        self.graphics = main.graphics
        self.events = main.events
        self.win = main.win
        self.main = main

    def start(self, args=None):
        self.scale()

        self.video = pyvidplayer2.Webcam(capture_size=(1920, 1080))
        self.video.change_resolution(RESY)

        self.thread = Thread(target=self.translate)
        self.results = None
        self.translated_text = None

    def translate(self):
        if self.video.frame_data is not None:
            d = self.video.frame_data.copy()

            self.results, self.translated_text = translator.get_information(d, "fr")

    def scale(self):
        pass

    def end(self):
        pass

    def update(self, dt):
        if self.events.resize:
            self.scale()

        if not self.thread.is_alive():
            self.thread = Thread(target=self.translate)
            self.thread.start()

        n = self.video.update()

        if self.results is not None and n:
            self.video.frame_surf = self.video._create_frame(
                translator.apply_information(self.video.frame_data, self.results, self.translated_text))

    def draw(self):
        self.win.blit(self.video.frame_surf, self.video.frame_surf.get_rect(center=self.win.get_rect().center).topleft)
