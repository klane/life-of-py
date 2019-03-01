from enum import Enum


class Seed(Enum):
    BLANK = {}

    # Seed for a 'Gosper Glider Gun' in set form.
    GOSPER = {(3, 22), (5, 17), (8, 16), (6,  2), (3, 35), (4, 16), (4, 36), (3, 14),
              (7, 25), (4, 22), (4, 21), (6, 18), (6,  1), (1, 25), (3, 36), (9, 13),
              (5,  2), (4, 35), (9, 14), (7, 17), (7, 11), (6, 17), (3, 13), (5, 11),
              (6, 25), (2, 23), (3, 21), (5,  1), (6, 15), (4, 12), (5, 21), (2, 25),
              (5, 22), (6, 23), (6, 11), (8, 12)}

    PULSAR = {(2,  4), (2,  5), (2,   6), (4,   2), (5,   2), (6,   2), (7,   4), (7,   5),
              (7,  6), (4,  7), (5,   7), (6,   7), (2,  10), (2,  11), (2,  12), (4,   9),
              (5,  9), (6,  9), (7,  10), (7,  11), (7,  12), (4,  14), (5,  14), (6,  14),
              (9,  4), (9,  5), (9,   6), (10,  2), (11,  2), (12,  2), (14,  4), (14,  5),
              (14, 6), (10, 7), (11,  7), (12,  7), (9,  10), (9,  11), (9,  12), (10,  9),
              (11, 9), (12, 9), (14, 10), (14, 11), (14, 12), (10, 14), (11, 14), (12, 14)}

    def __iter__(self):
        return self.value.__iter__()
