import itertools
import numpy as np
import sys

class call_PLST:
    def do(self, trainclass, predictions, train, plst, PLST_class):
        self.trainclass = trainclass
        self.prediction = predictions
        self.traindata = train
        self.plst = plst
        self.matrix, self.go_index, self.rat_index, self.go_index_reverse = self.matrix_trainclass()
        transformed_matrix, transform = self.call(PLST_class)
        predicted_matrix, protein_volgorde = self.predict(transformed_matrix)
        inverse_matrix = transform.inverseMap(predicted_matrix)
        predictions = {}
        for getal, eiwit in enumerate(protein_volgorde):
            go_termen = []
            for getal1, go in enumerate(inverse_matrix[getal, :]):
                if go > 0.3:
                    go_termen.append(self.go_index_reverse[getal1])
            predictions[eiwit] = go_termen
        return predictions


    def matrix_trainclass(self):
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
        return matrix, go_index, rat_index, go_index_reverse

    def call(self, PLST_class):
        transform = PLST_class()
        doorgaan = True
        while doorgaan:
            try:
                transformed_matrix = transform.fit(self.matrix, ndims=round(self.matrix.shape[1] / self.plst))
                doorgaan = False
            except:
                print("SVD error, conversion runs again ")
        return transformed_matrix, transform

    def predict(self, transformed):
        index = []
        protein_volgorde = []
        for key, value in self.traindata.items():
            for protein in value:
                if protein in self.rat_index:
                    protein_volgorde.append(key)
                    index.append(self.rat_index[protein])
        return transformed[index, :], protein_volgorde