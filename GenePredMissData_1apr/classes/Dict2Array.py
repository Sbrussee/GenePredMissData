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
        check_een = 0
        for id in data:
            if func != None:
                vals = func(data[id])
            else:
                vals = data[id]
            if len(vals) > 0:
                if type(vals[0]) == tuple:
                    if check_een == 0:
                        check_een = 10
                        create.set_rest(1, self.y_size, self.x_size )
                    create.get_extend(self.y_pos, self.x_pos, vals, id)
                else:
                    vals = vals[0]
                    if check_een == 0:
                        check_een = 10
                        create.set_rest(2, self.y_size, self.x_size )
                    create.get_not_extend(self.y_pos, self.x_pos, vals, id)
        return create.get_array()

class create_array():
    def __init__(self):
        self.res = []

    def set_rest(self, getal, y_size, x_size):
        if getal == 1:
            self.res = lil_matrix((y_size, x_size), dtype=float)
        else:
            self.res = lil_matrix((y_size, x_size), dtype=bool)

    def get_not_extend(self, y_pos, x_pos, vals, id):
        if id in y_pos and vals in x_pos:
            self.res[y_pos[id], x_pos[vals]] = True

    def get_extend(self, y_pos, x_pos, vals, id):
        for regels in vals:
            if id in y_pos and regels[0] in x_pos:
                self.res[y_pos[id], x_pos[regels[0]]] = regels[1]

    def get_array(self):
        return self.res







