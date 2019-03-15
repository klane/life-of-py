from enum import Enum
from functools import partial

import numpy as np


class Seed(Enum):
    # Blank slate
    BLANK = {}

    # Gosper glider gun
    GOSPER = {(3, 22), (5, 17), (8, 16), (6,  2), (3, 35), (4, 16), (4, 36), (3, 14),
              (7, 25), (4, 22), (4, 21), (6, 18), (6,  1), (1, 25), (3, 36), (9, 13),
              (5,  2), (4, 35), (9, 14), (7, 17), (7, 11), (6, 17), (3, 13), (5, 11),
              (6, 25), (2, 23), (3, 21), (5,  1), (6, 15), (4, 12), (5, 21), (2, 25),
              (5, 22), (6, 23), (6, 11), (8, 12)}

    # Oscillator with period 15
    PENTADECATHLON = {(3,  4), (3,  5), (3,  6), (4,  5), (5,  5), (6,  5), (6,  4), (6,  6),
                      (11, 4), (11, 5), (11, 6), (12, 5), (13, 5), (14, 5), (14, 4), (14, 6),
                      (8,  4), (8,  5), (8,  6), (9,  4), (9,  5), (9,  6)}

    # Oscillator with period 3
    PULSAR = {(2,  4), (2,  5), (2,   6), (4,   2), (5,   2), (6,   2), (7,   4), (7,   5),
              (7,  6), (4,  7), (5,   7), (6,   7), (2,  10), (2,  11), (2,  12), (4,   9),
              (5,  9), (6,  9), (7,  10), (7,  11), (7,  12), (4,  14), (5,  14), (6,  14),
              (9,  4), (9,  5), (9,   6), (10,  2), (11,  2), (12,  2), (14,  4), (14,  5),
              (14, 6), (10, 7), (11,  7), (12,  7), (9,  10), (9,  11), (9,  12), (10,  9),
              (11, 9), (12, 9), (14, 10), (14, 11), (14, 12), (10, 14), (11, 14), (12, 14)}

    # Random seed with discrete uniform distribution
    RANDOM = partial(np.random.randint, 2, dtype=bool)

    # Random seed with 25% probability of starting alive
    RANDOM_25 = partial(np.random.choice, [True, False], p=[0.25, 0.75])

    def __call__(self, *args, **kwargs):
        return self.value(*args, **kwargs)

    def __iter__(self):
        return self.value.__iter__()
