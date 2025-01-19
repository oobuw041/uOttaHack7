from colours import *
from config import *
import pygame


class Splash:
    def __init__(self, main):
        self.graphics = main.graphics
        self.events = main.events
        self.win = main.win
        self.main = main

    def start(self, args=None):
        self.scale()

        self.text_alpha = 255

        self.global_offset = -50

        self.student_center_pos = pygame.Rect(self.graphics.draw("student", (0, RESY // 2 + self.global_offset), center=pygame.Rect(0, 0, RESX // 2, RESY // 2))).center
        self.teacher_center_pos = pygame.Rect(self.graphics.draw("teacher", (0, RESY // 2 + self.global_offset), center=pygame.Rect(RESX // 2, 0, RESX // 2, RESY // 2))).center

        self.draw_x, self.draw_y = self.student_center_pos

        self.last_selection = 1

        self.student_rect = pygame.Rect(0, 0, *self.graphics.get_image("student").get_size())
        self.student_rect.center = self.student_center_pos
        self.teacher_rect = pygame.Rect(0, 0, *self.graphics.get_image("teacher").get_size())
        self.teacher_rect.center = self.teacher_center_pos

        self.transitioning = False
        self.target = ""
        self.transition_pos = (0, 0)
        self.transition_r = 0

    def scale(self):
        pass

    def end(self):
        pass

    def update(self, dt):
        if self.events.resize:
            self.scale()

        if self.transitioning:
            self.events.x = self.transition_pos[0]
            target = 800
            self.transition_r += (target + 10 - self.transition_r) / 10
            if self.transition_r > target:
                self.main.set_location(self.target)

        else:
            if int(self.events.x > RESX // 2) != self.last_selection:
                self.text_alpha = 0

            self.last_selection = int(self.events.x > RESX // 2)

            self.text_alpha += (255 - self.text_alpha) / 50

            if self.student_rect.collidepoint(self.events.mouse) and self.events.click:
                self.target = ""
                self.transitioning = True
                self.transition_pos = (self.draw_x, self.student_center_pos[1])
            elif self.teacher_rect.collidepoint(self.events.mouse) and self.events.click:
                self.target = "upload"
                self.transitioning = True
                self.transition_pos = (self.draw_x, self.student_center_pos[1])

    def draw(self):
        self.win.fill(BACK_COLOUR)

        rect = self.graphics.write(f"Welcome, I am a... {("student.", "professor.")[self.events.x > RESX // 2]}", (0, self.global_offset), center=pygame.Rect(0, 0, RESX, RESY // 2), size=50, font="Naturaly")
        self.graphics.write(f"{("Enjoy the lecture in your preferred language.", "Teach the class in your most comfortable language.")[self.events.x > RESX // 2]}", (0, self.global_offset), center=pygame.Rect(0, rect[1] + rect[3] + 50, RESX, 100), alpha=self.text_alpha, size=30, font="Naturaly")
        target_pos = (self.student_center_pos, self.teacher_center_pos)[self.events.x > RESX // 2]
        self.draw_x += (target_pos[0] - self.draw_x) / 8

        pygame.draw.circle(self.win, MAIN_COLOUR1, (self.draw_x, self.draw_y), 120)

        self.graphics.draw("student", (0, 0), center=self.graphics.draw("student", (0, RESY // 2 + self.global_offset), center=pygame.Rect(0, 0, RESX // 2, RESY // 2)))
        self.graphics.draw("teacher", (0, 0), center=self.graphics.draw("teacher", (0, RESY // 2 + self.global_offset), center=pygame.Rect(RESX // 2, 0, RESX // 2, RESY // 2)))

        if self.transitioning:
            pygame.draw.circle(self.win, MAIN_COLOUR1, self.transition_pos, self.transition_r)
