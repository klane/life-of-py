import os
import sys

import numpy as np
import pygame as pg
from scipy.signal import convolve2d
from seeds import *

CAPTION = "Conway"
FPS = 30
CELL_SIZE = 12
GRID_SIZE = (50, 100)
CELL_MARGIN = 2
BACKGROUND_COLOR = pg.Color("darkslategray")
VISITED_COLOR = [min(chan + 20, 255) for chan in BACKGROUND_COLOR]

BIRTH = tuple({3})
SURVIVE = tuple({2, 3})
SEED = GOSPER


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
        self.seed()

    def seed(self):
        for r, c in SEED:
            self.grid[r, c] = 1

    def set(self, coords, value):
        self.grid[coords] = value

    def reset(self):
        self.grid.fill(0)
        self.age.fill(0)
        self.seed()

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
        self.generation = 1

    def reset(self):
        self.background.fill(BACKGROUND_COLOR)
        self.grid.reset()
        self.generation = 1

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
            self.generation += 1

    def render(self):
        pg.display.set_caption(CAPTION + ': Generation ' + str(self.generation))
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
    size = GRID_SIZE[1] * CELL_SIZE, GRID_SIZE[0] * CELL_SIZE
    pg.display.set_mode(size)
    App().main_loop()
    pg.quit()
    sys.exit()


if __name__ == "__main__":
    main()
