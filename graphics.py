import pygame
import os
import cv2
from colours import *


class Graphics:
    def __init__(self, win):
        self.win = win

        self.fonts = {"arial": pygame.font.SysFont("arial", 30)}
        self.original_images = {}

        self._image_cache = {}
        self._font_paths = {}

    def load_folder(self, path="assets", size=None):
        for file in os.listdir(path):
            if os.path.isdir(os.path.abspath(os.path.join(path, file))):
                self.load_folder(os.path.join(path, file), size)
            else:
                if file.endswith(".ttf") or file.endswith(".otf"):
                    self.load_font(os.path.join(path, file))
                elif file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jpeg"):
                    self.load_image(os.path.join(path, file), size)

    def _quality_resize(self, image, size):
        if image.get_width() > size[0] and image.get_height() > size[1]:
            inter = cv2.INTER_AREA
        else:
            inter = cv2.INTER_LANCZOS4
        return pygame.image.frombuffer(
            cv2.resize(pygame.surfarray.pixels3d(image).swapaxes(0, 1), dsize=size, interpolation=inter).tobytes(),
            size, "RGB")

    def _fast_resize(self, image, size):
        return pygame.transform.scale(image, size)

    def _apply_ppa(self, image):
        surf = pygame.Surface(image.get_size(), pygame.SRCALPHA)
        surf.blit(image, (0, 0))
        return surf

    def load_font(self, path):
        f = os.path.splitext(os.path.split(path)[1])[0]
        self._font_paths[f] = path
        self.fonts[f + "30"] = pygame.font.Font(self._font_paths[f], 30)

    def load_image(self, path, size=None):
        i = os.path.splitext(os.path.split(path)[1])[0]
        self.original_images[i] = pygame.image.load(path).convert_alpha()
        if size is not None:
            self.resize(i, size)

    def resize_all(self, sizes):
        for image, size in sizes.items():
            if image in self.original_images:
                self.resize(image, size)

    def resize(self, image, size):
        self._image_cache[image] = self._quality_resize(self.original_images[image], size)

    def render_text(self, text, size=30, font="arial", colour=BLACK, alpha=None, angle=None):
        key = font + str(size)
        if not key in self.fonts:
            if font in self._font_paths:
                self.fonts[key] = pygame.font.Font(self._font_paths[font], size)
            else:
                self.fonts[key] = pygame.font.SysFont(font, size)

        surf = self.fonts[key].render(str(text), True, colour)

        if angle is not None:
            surf = pygame.transform.rotate(surf, angle)

        if alpha is not None:
            surf.set_alpha(alpha)

        return surf

    def write(self, text, pos, size=30, colour=BLACK, center=None, font="arial", alpha=None, angle=None, highlight=None,
              max_w=None):
        if max_w is None:
            surf = self.render_text(text, size, font, colour, alpha, angle)
        else:
            surfs = []
            space = self.render_text(" ", size, font, colour, alpha, angle)
            for word in text.split(" "):
                if word != "":
                    surfs.append(self.render_text(word, size, font, colour, alpha, angle))
                    surfs.append(space.copy())
            if surfs:
                del surfs[-1]

            longest_line = 0
            w = 0
            h = space.get_height()
            for surf in surfs:
                if w + surf.get_width() > max_w:
                    if surf.get_width() > max_w:
                        return (0, 0, 0, 0)
                    if w > longest_line:
                        longest_line = w
                    w = 0
                    h += space.get_height()
                w += surf.get_width()
            if w > longest_line:
                longest_line = w

            surf = pygame.Surface((longest_line, h))

            x = 0
            y = 0
            for s in surfs:
                if x + s.get_width() > longest_line:
                    x = 0
                    y += space.get_height()
                surf.blit(s, (x, y))
                x += s.get_width()

        if center is not None:
            pos = center[0] + center[2] / 2 - surf.get_width() / 2 + pos[0], pos[1] + center[1] + center[
                3] / 2 - surf.get_height() / 2

        if angle is not None:
            pos = surf.get_rect(center=pos).topleft

        r = (*pos, *surf.get_size())
        if highlight is not None:
            pygame.draw.rect(self.win, highlight, r)

        self.win.blit(surf, pos)

        return r

    def get_image(self, image, size=None, alpha=None, angle=None, copy=False):
        surf = self._image_cache[image] if image in self._image_cache else self.original_images[image]
        if copy:
            surf = surf.copy()

        if size is not None:
            self._image_cache[image] = surf = self._fast_resize(surf, size)

        if angle is not None:
            surf = pygame.transform.rotate(surf, angle)

        if alpha is not None:
            surf.set_alpha(alpha)

        return surf

    def draw(self, image, pos, angle=None, size=None, alpha=None, center=None):
        surf = self.get_image(image, size, alpha, angle)

        if center is not None:
            pos = center[0] + center[2] / 2 - surf.get_width() / 2 + pos[0], pos[1] + center[1] + center[
                3] / 2 - surf.get_height() / 2

        if angle is not None:
            pos = surf.get_rect(center=pos).topleft

        self.win.blit(surf, pos)

        return *pos, *surf.get_size()

    def get_highlight(self, size, rgba):
        s = pygame.Surface(size, pygame.SRCALPHA)
        s.fill(rgba)
        return s

    def apply_post(self, func):
        self.win.blit(pygame.image.frombuffer(
            func(pygame.surfarray.pixels3d(pygame.display.get_surface()).swapaxes(0, 1)).tobytes(), self.win.get_size(),
            "RGB"), (0, 0))
