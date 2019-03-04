# Conway's Game of Life

![screenshot](https://raw.githubusercontent.com/klane/life-of-py/master/assets/gosper-generation-100.png)

Generation 100 of a simulation seeded with the Gosper glider gun.

This project contains a Python implementation of [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) using [Pygame](https://www.pygame.org/). The number of each cell's neighbors are found using convolution with the kernel:

```
[1, 1, 1,
 1, 0, 1,
 1, 1, 1]
```

This work drew inspiration from [this project](https://github.com/Mekire/Conway-User-Interaction).

## Controls

- SPACE: Start/stop simulation
- TAB: Step to next generation (stops simulation if currently running)
- BACKSPACE: Reset simulation
