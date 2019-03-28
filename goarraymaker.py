import numpy as np

class GoArrayMaker:
    def __init__(self, go_tree, unicodes):
        """
        -go_tree: A dictionary containing all GO_ID's and their
                    parents.
        Predefines positions of all GO_therms based on go_tree.
        """
        unicodes = sorted(list(set(unicodes)))
        self.go_pos = {}
        self.y_pos = {}
        self.x_size = len(go_tree)
        self.y_size = len(unicodes)
        pos = 0
        for key in go_tree:
            self.go_pos[key] = pos
            pos += 1
        pos = 0
        for key in unicodes:
            self.y_pos[key] = pos
            pos += 1

    def make_go_array(self, data):
        """
        - data: Dictionary containing proteins and their GO_therms.
        Creates a boolean matrix of a protein - GO therm dataset.
        The x-positions are determined by go_pos and the y-Positions
        are determined by the dictionary order.
        - res: Numpy array containing a boolean matrix with proteins
                on the y-axis and GO_therms on the x-axis.
        """
        res = np.full((self.y_size, self.x_size), False, dtype=bool)
        for key in data:
            for go in data[key]:
                res[self.y_pos[key]][self.go_pos[go]] = True
        return res
