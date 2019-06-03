import numpy as np
import itertools
class train_matrix:
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

    def back_convert(self, matrix, rat_index, go_index_reverse, traindata):
        predictions = {}
        for mouse, rat in traindata.items():
            go = []
            for protein in rat:
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