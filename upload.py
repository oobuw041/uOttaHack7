import io
import math
import os.path
import time
from threading import Thread

import numpy as np
import pdf2image

from colours import *
from config import *
import pygame
import tkinter as tk
from tkinter import filedialog
import translator
from TestVoice2 import capture_and_translate

HERE_DEFAULT = BLUE
HERE_HIGHLIGHT = LIGHT_BLUE


class Upload:
    def __init__(self, main):
        self.graphics = main.graphics
        self.events = main.events
        self.win = main.win
        self.main = main

    def start(self, args=None):
        self.scale()

        self.translation_thread = Thread(target=capture_and_translate)

        offset = 130
        rect = self.graphics.write("Drag your lecture notes or press here to upload from your computer.", (0, offset),
                                   center=self.win.get_rect(), font="Naturaly", size=30)

        self.graphics.draw("file", (0, -50), center=self.win.get_rect(), alpha=128)

        rect = self.graphics.write("Drag your lecture notes or press ", (rect[0], rect[1]), font="Naturaly", size=30)
        rect = self.graphics.write("here", (rect[0] + rect[2], rect[1]), font="Naturaly", colour=BLUE)
        self.here_rect = pygame.Rect(*rect)

        self.here_colour = HERE_DEFAULT

        self.thread = Thread(target=lambda:None)
        self.loading_angle = 0
        self.rotation_timer = 0

        self.alpha = 0

        self.files = []

        self.transition_x = 0
        self.transitioning = False
        self.transitioned = False

        self.selected = None
        self.add_button = pygame.Rect(0, 0, 50, 50)

        self.editor_rect = pygame.Rect(RESX, 0, 0, RESY)

        self.dragging = False

        self.slide_cursor = pygame.cursors.compile(pygame.cursors.sizer_x_strings)
        self.slides = []

    def translate(self, file):
        self.rotation_timer = 0

        image = pdf2image.convert_from_path(file.path, last_page=1)[0]
        img = translator.translate_image(np.array(image), "fr")

        img = pygame.image.frombuffer(img, (img.shape[1], img.shape[0]), format="BGR")

        file.original_image = img

        ar = img.get_width() / img.get_height()
        w = self.editor_rect.w - 30
        h = w / ar

        file.image = pygame.transform.smoothscale(img, (w, h))
        file.size = w / img.get_width()

    def scale(self):
        pass

    def end(self):
        pass

    def update(self, dt):
        if self.events.resize:
            self.scale()

        self.alpha += 5
        if self.alpha > 255:
            self.alpha = 255

        if not self.files:
            self.here_colour = (HERE_DEFAULT, HERE_HIGHLIGHT)[self.here_rect.collidepoint(self.events.mouse)]
            if self.here_colour == HERE_HIGHLIGHT and self.events.click:
                path = self.get_files()
                if path != "":
                    self.files.append(File(path, self))
            elif self.events.file is not None:
                if self.events.file.endswith(".pdf"):
                    self.files.append(File(self.events.file, self))
        else:
            if not self.transitioned:
                self.transition_x = 0
                self.selected = self.files[-1]
                self.transitioned = True
                self.transitioning = True

            elif self.transitioning:
                self.transition_x += (RESX + 10 - self.transition_x) // 8
                self.editor_rect.w = self.transition_x
                self.editor_rect.x = RESX - self.transition_x
                if self.transition_x > RESX:
                    self.transitioning = False
                    self.editor_rect.w = RESX
                    self.editor_rect.x = 0
            # else:
            #     if abs(self.events.x - self.editor_rect.x) < 10:
            #         pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZEWE)
            #
            #         if self.events.click and not self.dragging:
            #             self.dragging = True
            #     else:
            #         pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            # if self.dragging:
            #     self.editor_rect.x = min(max(100, self.events.x), RESX - 180)
            #     self.editor_rect.w = RESX - self.editor_rect.x
            #     if not pygame.mouse.get_pressed()[0]:
            #         self.dragging = False
            # elif self.selected is not None:
            #     if self.editor_rect.collidepoint(self.events.mouse) and self.selected.original_image is not None:
            #         if self.events.scrolly != 0:
            #             self.selected.size += self.events.scrolly / 100
            #
            #             img = self.selected.original_image
            #
            #             ar = img.get_width() / img.get_height()
            #             w = max(30, self.selected.original_image.get_width() * self.selected.size)
            #             h = w / ar
            #
            #             self.selected.image = pygame.transform.smoothscale(img, (w, h))

            # for i, file in enumerate(self.files):
            #     file.update(i)
            #
            # self.add_button.bottomleft = self.win.get_rect().bottomleft

            # if self.add_button.collidepoint(self.events.mouse) and self.events.click:
            #     path = self.get_files()
            #     if path != "":
            #         self.files.append(File(path, self))
            # if self.events.file is not None:
            #     if self.events.file.endswith(".pdf"):
            #         self.files.append(File(self.events.file, self))


        self.rotation_timer += dt
        self.loading_angle += math.sin(self.rotation_timer / 1000) * 10

    def get_files(self):
        # Setting up the root window
        root = tk.Tk()
        root.withdraw()  # Hide the root window

        file_path = filedialog.askopenfilename(
            title="Select a PDF file",
            filetypes=[("PDF files", "*.pdf")]
        )

        return file_path

    def draw(self):
        if not self.files:
            offset = 130
            rect = self.graphics.write("Drag your lecture notes or press here to upload from your computer.", (0, offset),
                                       center=self.win.get_rect(), font="Naturaly", size=30)

            self.win.fill(MAIN_COLOUR1)
            self.graphics.draw("file", (0, -50), center=self.win.get_rect(), alpha=min(128, self.alpha))

            rect = self.graphics.write("Drag your lecture notes or press ", (rect[0], rect[1]), font="Naturaly", size=30, alpha=self.alpha)
            rect = self.graphics.write("here", (rect[0] + rect[2], rect[1]), font="Naturaly", colour=self.here_colour, alpha=self.alpha)
            self.graphics.write(" to upload from your computer.", (rect[0] + rect[2], rect[1]), font="Naturaly", alpha=self.alpha)
        else:
            self.win.fill(MAIN_COLOUR1)

            for file in self.files:
                file.draw()
                if not self.thread.is_alive() and file.image is None:
                    self.thread = Thread(target=self.translate, args=(file,))
                    self.thread.start()

            # self.graphics.draw("newplus", (0, 0), center=self.add_button)

            pygame.draw.rect(self.win, BACK_COLOUR, self.editor_rect)
            # pygame.draw.line(self.win, BLACK, self.editor_rect.topleft, self.editor_rect.bottomleft, 3)

            # pygame.draw.circle(self.win, BACK_COLOUR, self.win.get_rect().center, abs(180 - self.loading_angle))

            if self.selected is not None:
                if self.selected.image is None:
                    img = self.graphics.get_image("loading hrgls")
                    img = pygame.transform.rotate(img, self.loading_angle)
                    rect = img.get_rect(center=self.editor_rect.center)
                    self.win.blit(img, rect.topleft)

                    self.graphics.write("Translating file...", (0, -200), center=self.editor_rect, font="Naturaly")
                else:
                    self.win.blit(self.selected.image, (self.editor_rect.x + 15, self.editor_rect.y + 15))

                    if not self.translation_thread.is_alive():
                        self.translation_thread = Thread(target=capture_and_translate)
                        self.translation_thread.start()


FILE_H = 50
FILE_SPACING = 10
FILE_OFFSET = (40, 40)


class File:
    def __init__(self, path, location):
        self.path = path
        self .name = os.path.basename(path)
        self.location = location
        self.rect = pygame.Rect(0, 0, self.location.graphics.render_text(self.name, 30, "Naturaly", BLACK, None, None).get_width() + 30, FILE_H)
        self.image = None
        self.original_image = None
        self.size = 1

        self.anim = 0

    def update(self, i):
        self.rect.topleft = FILE_OFFSET[0], FILE_OFFSET[1] + (FILE_H + FILE_SPACING) * i

        # self.anim += (self.rect.h * self.rect.collidepoint(self.location.events.mouse) - self.anim) // 10
        #
        # if self.rect.collidepoint(self.location.events.mouse) and self.location.events.click and not self.location.editor_rect.collidepoint(self.location.events.mouse):
        #     if self.location.selected is self:
        #         self.location.selected = None
        #     else:
        #         self.location.selected = self

    def draw(self):
        # pygame.draw.rect(self.location.win, RED if self.location.selected is self else BACK_COLOUR, self.rect, 0, 8)
        # # pygame.draw.rect(self.location.win, MAIN_COLOUR1, (*self.rect.topleft, self.rect.w, self.anim), 0, 8)
        #
        # self.location.graphics.write(self.name, (0, 0), center=self.rect, font="Naturaly")
        pass