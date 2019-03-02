import pygame as pg
from seeds import Seed

# App options
CAPTION = 'Conway'
FPS = 30
WRAP = True

# Simulation options
BIRTH = tuple({3})  # number of neighbors for a cell to be born
SURVIVE = tuple({2, 3})  # number of neighbors for a cell to survive to the next generation
SEED = Seed.GOSPER

# Cell options
CELL_SIZE = 12
CELL_MARGIN = 2  # amount to shrink cells by to show spacing between cells

# Grid options
GRID_SIZE = (50, 100)  # (rows, columns)
SHOW_GRID = True

# Color options
CELL_COLOR = pg.Color('tomato')
GRID_COLOR = pg.Color('black')
BACKGROUND_COLOR = pg.Color('darkslategray')
VISITED_COLOR = [min(chan + 25, 255) for chan in BACKGROUND_COLOR]
