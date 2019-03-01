import os
import sys

import numpy as np
import pygame as pg
from scipy.signal import convolve2d

CAPTION = "Conway"
FPS = 30
CELL_SIZE = 12
GRID_SIZE = (50, 100)
CELL_MARGIN = 2
BACKGROUND_COLOR = pg.Color("darkslategray")
VISITED_COLOR = [min(chan + 20, 255) for chan in BACKGROUND_COLOR]

BIRTH = tuple({3})
SURVIVE = tuple({2, 3})

# Seed for a 'Gosper Glider Gun' in set form.
SEED = {(22, 3), (17, 5), (16, 8), (2, 6), (35, 3), (16, 4), (36, 4), (14, 3),
        (25, 7), (22, 4), (21, 4), (18, 6), (1, 6), (25, 1), (36, 3), (13, 9),
        (2, 5), (35, 4), (14, 9), (17, 7), (11, 7), (17, 6), (13, 3), (11, 5),
        (25, 6), (23, 2), (21, 3), (1, 5), (15, 6), (12, 4), (21, 5), (25, 2),
        (22, 5), (23, 6), (11, 6), (12, 8)}


class Cell(object):
    def __init__(self, coords):
        self.color = pg.Color("tomato")
        self.rect = pg.Rect((coords[0] * CELL_SIZE, coords[1] * CELL_SIZE),
                            (CELL_SIZE, CELL_SIZE))
        self.rect.inflate_ip(-CELL_MARGIN, -CELL_MARGIN)
        self.age = 0

    def draw(self, surface, background):
        color = [min(chan + self.age, 255) for chan in self.color]
        surface.fill(color, self.rect)
        background.fill(VISITED_COLOR, self.rect)


class Grid(object):
    def __init__(self):
        self.kernel = np.asarray([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
        self.grid = np.zeros(GRID_SIZE, dtype=bool)
        self.age = np.zeros(GRID_SIZE, dtype=int)

        for c, r in SEED:
            self.grid[r, c] = True
            self.age[r, c] = 1

    def set(self, coords, value):
        self.grid[coords] = value

    def reset(self):
        self.grid.fill(0)
        self.age.fill(0)

        for c, r in SEED:
            self.grid[r, c] = 1

    def update(self):
        neighbors = convolve2d(self.grid, self.kernel, mode='same', boundary='wrap')
        self.grid = (np.isin(neighbors, SURVIVE) & self.grid) | np.isin(neighbors, BIRTH)
        self.age[self.grid] += 1
        self.age[np.logical_not(self.grid)] = 0

    def draw(self, surface, background):
        for r, c in zip(*self.grid.nonzero()):
            cell = Cell((c, r))
            cell.age = self.age[r, c]
            cell.draw(surface, background)


class App(object):
    def __init__(self):
        self.grid = Grid()
        self.screen = pg.display.get_surface()
        self.background = pg.Surface(self.screen.get_size())
        self.background.fill(BACKGROUND_COLOR)
        self.fps = FPS
        self.clock = pg.time.Clock()
        self.done = False
        self.wrapping = True
        self.generating = False

    def reset(self):
        self.background.fill(BACKGROUND_COLOR)
        self.grid.reset()

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.generating = not self.generating
                elif event.key == pg.K_BACKSPACE:
                    self.reset()

    def add_delete(self, mouse):
        mouse_pos = pg.mouse.get_pos()
        coords = mouse_pos[1] // CELL_SIZE, mouse_pos[0] // CELL_SIZE

        if mouse[0]:
            self.grid.set(coords, 1)
        elif mouse[2]:
            self.grid.set(coords, 0)

    def update(self):
        mouse = pg.mouse.get_pressed()

        if any(mouse):
            self.add_delete(mouse)
        elif self.generating:
            self.grid.update()

    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.grid.draw(self.screen, self.background)
        pg.display.update()

    def main_loop(self):
        while not self.done:
            self.event_loop()
            self.update()
            self.render()
            self.clock.tick(self.fps)


def main():
    os.environ["SDL_VIDEO_CENTERED"] = "True"
    pg.init()
    pg.display.set_caption(CAPTION)
    size = GRID_SIZE[1] * CELL_SIZE, GRID_SIZE[0] * CELL_SIZE
    pg.display.set_mode(size)
    App().main_loop()
    pg.quit()
    sys.exit()


if __name__ == "__main__":
    main()
