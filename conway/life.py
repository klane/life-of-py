import os
import sys

import numpy as np
from itertools import product
from scipy.signal import convolve2d
from options import *


class Grid(object):
    def __init__(self):
        self.kernel = np.asarray([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
        self.grid = np.zeros(GRID_SIZE, dtype=bool)
        self.age = np.zeros(GRID_SIZE, dtype=int)
        self.padding = 0 if WRAP else 100

        if not WRAP:
            self.grid = np.pad(self.grid, self.padding, 'constant')

        self.seed()

    def seed(self):
        if SEED is Seed.RANDOM:
            rand = np.random.randint(2, size=GRID_SIZE, dtype=bool)

            if WRAP:
                self.grid = rand
            else:
                self.grid[self.padding:-self.padding, self.padding:-self.padding] = rand
        else:
            for r, c in SEED:
                self.grid[r + self.padding, c + self.padding] = 1

    def set(self, coords, value):
        self.grid[tuple([c + self.padding for c in coords])] = value

    def reset(self):
        self.grid.fill(0)
        self.age.fill(0)
        self.seed()

    def update(self):
        boundary = 'wrap' if WRAP else 'fill'
        neighbors = convolve2d(self.grid, self.kernel, mode='same', boundary=boundary)
        self.grid = (np.isin(neighbors, SURVIVE) & self.grid) | np.isin(neighbors, BIRTH)
        sub = self.unpad()
        self.age[sub] += 1
        self.age[np.logical_not(sub)] = 0

    def unpad(self):
        if WRAP:
            return self.grid
        else:
            return self.grid[self.padding:-self.padding, self.padding:-self.padding]

    def draw(self, screen, background):
        for r, c in zip(*self.unpad().nonzero()):
            rect = pg.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            rect.inflate_ip(-CELL_MARGIN, -CELL_MARGIN)
            color = [min(chan + self.age[r, c], 255) for chan in CELL_COLOR]
            screen.fill(color, rect)
            background.fill(VISITED_COLOR, rect)


class App(object):
    def __init__(self):
        self.size = GRID_SIZE[1] * CELL_SIZE, GRID_SIZE[0] * CELL_SIZE
        self.screen = pg.display.set_mode(self.size)
        self.background = pg.Surface(self.size)
        self.background.fill(BACKGROUND_COLOR)
        self.grid = Grid()
        self.clock = pg.time.Clock()
        self.done = False
        self.generating = False
        self.generation = 1

        if SHOW_GRID:
            self.draw_grid()

    def draw_grid(self):
        for r, c in product(range(GRID_SIZE[0]+1), range(GRID_SIZE[1]+1)):
            x = c * CELL_SIZE - CELL_MARGIN / 4
            y = r * CELL_SIZE - CELL_MARGIN / 4
            pg.draw.line(self.background, GRID_COLOR, (x, 0), (x, self.size[1]), CELL_MARGIN)
            pg.draw.line(self.background, GRID_COLOR, (0, y), (self.size[0], y), CELL_MARGIN)

    def reset(self):
        self.background.fill(BACKGROUND_COLOR)
        self.grid.reset()
        self.generation = 1

        if SHOW_GRID:
            self.draw_grid()

    def event_loop(self):
        for event in pg.event.get():
            if event.type is pg.QUIT:
                self.done = True
            elif event.type is pg.KEYDOWN:
                self.handle_key(event.key)

    def handle_key(self, key):
        if key is pg.K_SPACE:
            self.generating = not self.generating
        elif key is pg.K_TAB:
            self.generating = False
            self.step()
        elif key is pg.K_BACKSPACE:
            self.reset()

    def add_delete(self, mouse):
        mouse_pos = pg.mouse.get_pos()
        coords = mouse_pos[1] // CELL_SIZE, mouse_pos[0] // CELL_SIZE

        if mouse[0]:
            self.grid.set(coords, 1)
        elif mouse[2]:
            self.grid.set(coords, 0)

    def step(self):
        self.grid.update()
        self.generation += 1

    def update(self):
        mouse = pg.mouse.get_pressed()

        if any(mouse):
            self.add_delete(mouse)
        elif self.generating:
            self.step()

    def render(self):
        pg.display.set_caption(CAPTION + ': Generation ' + str(self.generation))
        self.screen.blit(self.background, (0, 0))
        self.grid.draw(self.screen, self.background)
        pg.display.update()

    def start(self):
        while not self.done:
            self.event_loop()
            self.update()
            self.render()
            self.clock.tick(FPS)


def main():
    os.environ['SDL_VIDEO_CENTERED'] = 'True'
    pg.init()
    App().start()
    pg.quit()
    sys.exit()


if __name__ == '__main__':
    main()
