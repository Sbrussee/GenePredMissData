import numpy as np
from scipy.sparse import *
from scipy import *


class Dict2Array:
    def __init__(self, x, y, extend):
        self.extend = extend
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


    def make_array(self, data, func=None):
        parse_matrix = []
        if self.extend == 1:
            parse_matrix = make_array_not_extend(self, data, func)
        elif self.extend > 1:
            parse_matrix = make_array_extend(self, data, func)
        return parse_matrix

def make_array_extend(self, data, func):
    parse_matrix = []
    for key in data.values():
        if len(key) > 0:
            if type(key[1]) == tuple:
                parse_matrix = train_extend(self, data, func)
                break
            else:
                parse_matrix = test_extend(self, data, func)
                break
    return parse_matrix

def train_extend(self, data, func):
    res = lil_matrix((self.y_size, self.x_size), dtype=float)
    for key in data:
        if func != None:
            vals = func(data[key])
        else:
            vals = data[key]
        for value in vals:
            if not key in self.y_pos:
                # print("Err key '%s' not in y index."%key)
                continue
            if not value[0] in self.x_pos:
                print("Err value '%s' not in x index." % value[0])
                res[self.y_pos[key], self.x_pos[value[0]]] = 0
                continue
            res[self.y_pos[key], self.x_pos[value[0]]] = value[1]

    return res


def test_extend(self, data, func):
    res = lil_matrix((self.y_size, self.x_size), dtype=float)
    for key in data:
        if func != None:
            vals = func(data[key])
        else:
            vals = data[key]
        for value in vals:
            if not key in self.y_pos:
                # print("Err key '%s' not in y index."%key)
                continue
            if not value in self.x_pos:
                print("Err value '%s' not in x index." % value)
                continue
            res[self.y_pos[key], self.x_pos[value]] = 1
    return res


def make_array_not_extend(self, data, func):
    # res = np.full((self.y_size, self.x_size), False, dtype=bool)
    res = lil_matrix((self.y_size, self.x_size), dtype=bool)
    for key in data:
        if func != None:
            vals = func(data[key])
        else:
            vals = data[key]
        for value in vals:
            if not key in self.y_pos:
                # print("Err key '%s' not in y index."%key)
                continue
            if not value in self.x_pos:
                print("Err value '%s' not in x index." % value)
                continue
            res[self.y_pos[key], self.x_pos[value]] = True
    return res


if __name__ == "__main__":
    x = ["GO:1", "GO:2", "GO:3"]
    y = ["PROT1", "PROT2", "PROT3"]
    data = {"PROT1": ["GO:1", "GO:3"], "PROT2": ["GO:2"], "PROT3": ["GO:3"]}

    arrmaker = Dict2Array(x, y, 1)
    array = arrmaker.make_array(data)
