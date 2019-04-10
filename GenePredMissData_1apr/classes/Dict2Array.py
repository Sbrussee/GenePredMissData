import numpy as np
from scipy.sparse import *
from scipy import *


class Dict2Array:
    def __init__(self, x, y, dtype):
        self.dtype = dtype
        x = sorted(list(set(x)))
        y = sorted(list(set(y)))
        self.x_pos = {key:getal for getal, key in enumerate(x)}
        self.y_pos = {key:getal for getal, key in enumerate(y)}
        self.x_size = len(x)
        self.y_size = len(y)

    def make_array(self, data, func):
        res = lil_matrix((self.y_size, self.x_size), dtype=self.dtype)
        for key in data:
            if func != None:
                vals = func(data[key])
            else:
                vals = data[key]
            for value in vals:
                if not type(value) == tuple:
                    value = (value, True)
                if not key in self.y_pos:
                    continue
                if not value[0] in self.x_pos:
                   # print("Err value '%s' not in x index." % value[0])
                    continue
                res[self.y_pos[key], self.x_pos[value[0]]] = value[1]
        return res