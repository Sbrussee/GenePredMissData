import numpy as np
from scipy.sparse import *
from scipy import *

# This class has been made to create a matrix from the input data(test and train set).
class Dict2Array:

    # The x: all go terms, y: All protein ids, dtype: Defining type array, must be imported.
    # All data from the x, y will be saved in a dictionairy assigned with a position.
    # Also, the size of each dictionairy will be defined.
    def __init__(self, x, y):
        self.dtype = dtype
        x = sorted(list(set(x)))
        y = sorted(list(set(y)))
        self.x_pos = {key:getal for getal, key in enumerate(x)}
        self.y_pos = {key:getal for getal, key in enumerate(y)}
        self.x_size = len(x)
        self.y_size = len(y)

    # This function creates the matrix with the data(train or prediction data). Also the go term tree must
    # be imported to get all go terms for a specific go term.
    # First, the matrix will be defined.
    # Second, for all ids the go terms will be specified.
    # Thirdly, if the go term in the go term dictionry and protein id in protein dictionairy defined above, then
    # fill the matrix.
    def make_array(self, data, func):
        res = lil_matrix((self.y_size, self.x_size), dtype=self.dtype)
        #file = open("print", "a")
        #file.write("Print\n")
        #file.close()

    def make_array(self, data, func, dtype):
        res = lil_matrix((self.y_size, self.x_size), dtype=dtype)
        for key in data:
            if func != None:
                vals = func(data[key])
            else:
                vals = data[key]
            #file = open("print", "a")
            #file.write("TUPLE:" + str(data[key]))
            #if type(data[key][0]) == tuple:
            #    file.write("BEFORE GOFIX:"+  str(data[key]) + "\n")
            #    file.write("AFTER GOFIX:" + str(vals) + "\n")
            #file.close()
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

    def get_index(self):
        return self.x_pos, self.y_pos
