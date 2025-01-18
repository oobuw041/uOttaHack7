import pygame


class Events:
    def __init__(self, fps, alt_f4=True, alt_enter=False, escape=False) -> None:
        self.alt_f4 = alt_f4
        self.alt_enter = alt_enter
        self.escape = escape
        self.fps = fps

        self._clock = pygame.time.Clock()

        self.update()

    def update(self):
        self.x, self.y = self.mouse = pygame.mouse.get_pos()
        self.mouse_down = pygame.mouse.get_pressed()
        self.keys_down = pygame.key.get_pressed()

        self.quit = False
        self.toggle = False

        self.input = None
        self.input_id = None
        self.input_unicode = None
        self.click = False
        self.right_click = False
        self.resize = False
        self.size = (0, 0)
        self.scrollx = self.scrolly = 0
        self.file = None
        self.mouse_move = (0, 0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.click = True
                elif event.button == 3:
                    self.right_click = True
            elif event.type == pygame.KEYDOWN:
                self.input = pygame.key.name(event.key)
                self.input_id = event.key
                self.input_unicode = event.unicode
            elif event.type == pygame.VIDEORESIZE:
                self.resize = True
                self.size = event.w, event.h
            elif event.type == pygame.MOUSEWHEEL:
                self.scrollx = event.x
                self.scrolly = event.y
            elif event.type == pygame.DROPFILE:
                self.file = event.file
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_move = event.pos

        if self.escape and self.input == "escape":
            self.quit = True

        if pygame.key.get_mods() & pygame.KMOD_ALT:
            if self.alt_f4 and self.input == "f4":
                self.quit = True
            elif self.alt_enter and self.input == "return":
                self.toggle = True

        return self._clock.tick(self.fps)

    def get_fps(self):
        return round(self._clock.get_fps())

# get directional vector
# return self.keys_down[right] - self.keys_down[left], self.keys_down[down] - self.keys_down[up]
