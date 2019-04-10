import numpy as np
from scipy.sparse import *
from scipy import *


class Dict2Array:
    def __init__(self, x, y, dtype):
        self.dtype = dtype
        x = sorted(list(set(x)))
        y = sorted(list(set(y)))
        self.x_pos = {}
        self.y_pos = {}
        self.x_size = len(x)
        self.y_size = len(y)
        pos = 0
        for key in x:
            self.x_pos[key] = pos
            pos += 1
        pos = 0
        for key in y:
            self.y_pos[key] = pos
            pos += 1


    def make_array(self, data, func):
        for value in data.values():
            if value != []:
                t = value[0][0]
                break
        if type(t) == tuple:
            t = type(t[1])
        else:
            t = bool
        res = lil_matrix((self.y_size, self.x_size), dtype=t)
        for key in data:
            if func != None:
                vals = func(data[key])
            else:
                vals = data[key]
            for value in vals:
                if not type(value) == tuple:
                    value = (value, True)
                    #print(value)
                if not key in self.y_pos:
                    continue
                if not value[0] in self.x_pos:
                    print("Err value '%s' not in x index." % value[0])
                    continue
                res[self.y_pos[key], self.x_pos[value[0]]] = value[1]
        return res


if __name__ == "__main__":
    x = ["GO:1", "GO:2", "GO:3"]
    y = ["PROT1", "PROT2", "PROT3"]
    data = {"PROT1": ["GO:1", "GO:3"], "PROT2": ["GO:2"], "PROT3": ["GO:3"]}

    arrmaker = Dict2Array(x, y, 1)
    array = arrmaker.make_array(data)
