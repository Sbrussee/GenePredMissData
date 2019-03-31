import numpy as np

class Converter:
    def __init__(self, unique):
        self.unique = unique
        self.lengte = 0

    def fill_np(self, lengte, true_data, true_ids):
        self.lengte = lengte
        true_array = np.zeros((self.lengte, len(self.unique)), dtype="int")
        for id, terms in true_data.items():
            for term in terms:
                true_array[true_ids[id], self.unique[term]] = 1
        return true_array


    def set_training_np(self, data, true_ids):
        self.training = np.zeros((self.lengte, len(self.unique)), dtype="int")
        for id, terms in data.items():
            for term in terms:
                self.training[true_ids[id], self.unique[term]] = 1
        return self.training
