from enum import Enum


class Seed(Enum):
    BLANK = {}

    # Seed for a 'Gosper Glider Gun' in set form.
    GOSPER = {(3, 22), (5, 17), (8, 16), (6,  2), (3, 35), (4, 16), (4, 36), (3, 14),
              (7, 25), (4, 22), (4, 21), (6, 18), (6,  1), (1, 25), (3, 36), (9, 13),
              (5,  2), (4, 35), (9, 14), (7, 17), (7, 11), (6, 17), (3, 13), (5, 11),
              (6, 25), (2, 23), (3, 21), (5,  1), (6, 15), (4, 12), (5, 21), (2, 25),
              (5, 22), (6, 23), (6, 11), (8, 12)}
