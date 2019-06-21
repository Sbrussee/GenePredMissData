import numpy as np
import itertools


"""
Class: To create a matrix and a index for the gaf file.
"""
class train_matrix:

    """
    Function: To create the matrix and an index.
    self.trainclass: All annotation information for the train gaf file.
    go_termen_train: A list of all unique go terms in the train gaf.
    go_index: To index all the go terms in a dictionaire.
    matrix: To create a matrix with on the y-axis the train genes and on the x-axis the go terms.
    return: The matrix with the go termen en gen index.
    """
    def convert(self, train_class):
        self.trainclass = train_class
        go_termen_train = [go for go in self.trainclass.values()]
        go_termen_train = list(itertools.chain.from_iterable(go_termen_train))
        go_termen_train = np.unique(go_termen_train)
        go_index = {a: getal for getal, a in enumerate(np.unique(go_termen_train))}
        go_index_reverse = {getal: a for getal, a in enumerate(np.unique(go_termen_train))}

        # Step 2: Create matrix from all unique go terms in gaf file
        matrix = np.zeros(((len(self.trainclass), len(go_termen_train))), dtype="int")
        rat_index = {}
        getal = 0
        for rat, go_terms in self.trainclass.items():
            rat_index[rat] = getal
            for go in go_terms:
                index = go_index[go]
                matrix[getal, index] = 1
            getal += 1
        return matrix, go_index_reverse, rat_index

    """
    function: To put the predicted matrix into a dictionaire.
    predicitions: To put the matrix in a dictionaire. 
    1. The function iterate over the train data.
    2. if the protein occurs in the prediction then the protein with go terms are stored in the matrix. 
    """
    def back_convert(self, matrix, rat_index, go_index_reverse, traindata):
        predictions = {}
        for mouse, rat in traindata.items():
            go = []
            print(rat)
            for protein in rat:
                if protein in rat_index:
                    matrix_index = rat_index[protein]
                    i = np.where(matrix[matrix_index] > 0.3)[0]
                    for go_terms in i:
                        go.append(go_index_reverse[go_terms])
            if len(rat) == 1:
                predictions[mouse] = go
            elif len(rat) > 1:
                unique, counts = np.unique(go, return_counts=True)
                predictions[mouse] = list(zip(unique, counts / len(rat)))
        return predictions