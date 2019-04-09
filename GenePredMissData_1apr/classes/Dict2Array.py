import numpy as np
from scipy.sparse import *
from scipy import *


class Dict2Array:
    def __init__(self, x, y, extend):
        self.extend = extend
        self.x_pos = {key:pos for pos, key in enumerate(x)}
        self.y_pos = {key:pos for pos, key in enumerate(y)}
        self.x_size = len(x)
        self.y_size = len(y)


    def make_array(self, data, func):
        create = create_array()
        for id, value in data.items():

            if func != None:
                vals = func(data[id])
            else:
                vals = func(data[id])

            if len(value) > 0:
                if type(value[0]) == tuple:
                    res = create.get_extend(self.y_size, self.x_size, value, self.y_pos, self.x_pos, vals, id)
                else:
                    res = create.get_not_extend(self.y_size, self.x_size, self.y_pos, self.x_pos, vals, id)
        return res

class create_array():
    @staticmethod
    def get_not_extend(y_size, x_size, y_pos, x_pos, vals, id):
        res = lil_matrix((y_size, x_size), dtype=bool)
        for val in vals:
            if id in y_pos and val in x_pos:
                res[y_pos[id], x_pos[val]] = True
        return res


    @staticmethod
    def get_extend(y_size, x_size, value, y_pos, x_pos, vals, id):
        res = lil_matrix((y_size, x_size), dtype=float)
        for val in vals:
            for regels in value:
                print(regels)
                if id in y_pos and val in x_pos:
                    res[y_pos[id], x_pos[val]] = regels[1]
        return res






