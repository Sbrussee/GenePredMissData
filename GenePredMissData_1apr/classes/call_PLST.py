import itertools
import numpy as np
import sys


"""
Class: To perform the PLST method.
"""
class call_PLST:
    
    """
    Function: To transform the annotation matrix.
    self.transformed_matrix: the transformed matrix. 
    """
    def train(self, train_matrix, plst, PLST_class):
        self.train_matrix = train_matrix
        self.plst = plst
        self.transformed_matrix, self.transform = self.call(PLST_class)
        return self.transformed_matrix

    """
    Function: to transform the matrix
    transformed_matrix: The transformed matrix
    transform: The PLST class
    """
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

    """
    Function: To convert the transformed matrix back to get the original values.
    inversed_matrix: The matrix which is transformed back
    """
    def inverse(self, matrix):
        inversed_matrix = self.transform.inverseMap(matrix)
        return inversed_matrix

