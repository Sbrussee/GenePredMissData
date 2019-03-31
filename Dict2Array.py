import numpy as np

class Dict2Array:
    def __init__(self, x, y):
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

    def make_array(self, data):
        res = np.full((self.y_size, self.x_size), 0)
        for key in data:
            for value in data[key]:
                if value in self.x_pos:
                    res[self.y_pos[key]][self.x_pos[value]] = 1
        return res


if __name__ == "__main__":
    x = ["GO:1", "GO:2", "GO:3"]
    y = ["PROT1", "PROT2", "PROT3"]
    data = {"PROT1":["GO:1", "GO:3"], "PROT2":["GO:2"], "PROT3": ["GO:3"]}
    arrmaker = Dict2Array(x, y)
    array = arrmaker.make_array(data)
    print(array)
