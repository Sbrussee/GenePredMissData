import itertools
import numpy as np
import sys

class call_PLST:
    def train(self, train_matrix, plst, PLST_class):
        self.train_matrix = train_matrix
        self.plst = plst
        self.transformed_matrix, self.transform = self.call(PLST_class)
        return self.transformed_matrix


    def call(self, PLST_class):
        transform = PLST_class()
        doorgaan = True
        while doorgaan:
            try:
                transformed_matrix = transform.fit(self.train_matrix, ndims=round(self.train_matrix.shape[1] / self.plst))
                doorgaan = False
            except:
                print("SVD error, conversion runs again ")
        return transformed_matrix, transform

    def inverse(self, matrix):
        inversed_matrix = self.transform.inverseMap(matrix)
        return inversed_matrix

