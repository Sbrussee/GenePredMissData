import numpy as np
from scipy.sparse import lil_matrix as lil
import sys
import itertools

# This class is to predict if only the blast besthit method is used.
class Predictor:

    # Traindata must be imported and the blast results will be saved into the traindata dictionaire.
    def __init__(self, traindata, args):
        self.traindata = {}
        for line in traindata:
            line = line.split("\t")
            if len(line) > 1:
                self.traindata[line[0]] = line[1]


    # This function saves the gaf file from the train set(rat gaf)
    def set_trainclass(self, trainclass, PLST):
        if PLST:
            # Step 1: Determine how big the matrix will be.
            self.go_termen_train = [go for go in trainclass.values()]
            self.go_termen_train = list(itertools.chain.from_iterable(self.go_termen_train))
            self.go_termen_train = np.unique(self.go_termen_train)
            self.go_index = {a:getal for getal, a in enumerate(np.unique(self.go_termen_train))}
            self.go_index_reverse = {getal: a for getal, a in enumerate(np.unique(self.go_termen_train))}
            self.train_id_reverse = {getal: id for getal, id in enumerate(trainclass)}

            # Step 2: Create matrix from all unique go terms in gaf file
            self.matrix = np.zeros(((len(trainclass), len(self.go_termen_train))), dtype="int")
            self.rat_index = {}
            getal = 0
            for rat, go_terms in trainclass.items():
                self.rat_index[rat] = getal
                for go in go_terms:
                    index = self.go_index[go]
                    self.matrix[getal, index] = 1
                getal += 1


        else:
            global train
            train = trainclass
            self.trainclass = trainclass


    # The testdata must be imported.
    # First, the loop will look if the id from the testdata is in the blast results dictionaire: self.traindata.
    # Second, the loop will look if the linked train id to the test id can be linked to the train gaf file.
    # Third, if so save the data.
    def get_predictions(self, testdata, PLST, PLST_class):
        predictions = {}
        if PLST:
            transformed_matrix, transform = call_PLST_class(self, PLST_class)
            predicted_matrix, protein_volgorde = PLST_predictions(self, testdata, transformed_matrix)
            inverse_matrix = transform.inverseMap(predicted_matrix)
            # Zet de predictions weer terug in een dictionairy
            for getal, eiwit in enumerate(protein_volgorde):
                go_termen = []
                for getal1, go in enumerate(inverse_matrix[getal, : ]):
                    if go > 0.3:
                        go_termen.append(self.go_index_reverse[getal1])
                predictions[eiwit] = go_termen
        else:
            predictions = not_PLST_predictions(self, testdata)
        return predictions

    # If this method is used, return a bool for defining which type of array has to be made.
    def get_dtype(self):
        return bool

# Predictions if PLST
def PLST_predictions(self, testdata, transformed):
    index = []
    protein_volgorde = []
    for protein in testdata:
        protein = protein.strip()
        if protein in self.traindata:
            check = self.traindata[protein].strip()
            if check in self.rat_index:
                protein_volgorde.append(protein)
                index.append(self.rat_index[check])
    return transformed[index, :], protein_volgorde

# Call PLST class
def call_PLST_class(self, PLST_class):
    getal = int("%.0f" % (self.matrix.shape[1] / 4))
    transform = PLST_class()
    try:
        transformed_matrix = transform.fit(self.matrix, ndims=getal)
    except:
        print("plst methode werkt niet op matrix: ", self.matrix.shape)
        sys.exit()
    return transformed_matrix, transform

# Method if not PLST method is used
def not_PLST_predictions(self, testdata):
    predictions = {}
    for protein in testdata:
        protein = protein.strip()
        if protein in self.traindata:
            protein_class = self.traindata[protein].strip()
            if protein_class in self.trainclass:
                predictions[protein] = self.trainclass[protein_class]
    return predictions


# Klopt de script?
if __name__ == "__main__":
    trainclass = {'A1': ['GO:1', 'GO:2', 'GO:3', 'GO:4', 'GO:5'],
                  'A2': ['GO:1', 'GO:2'],
                  'A3': ['GO:1', 'GO:2', 'GO:3', 'GO:4', 'GO:5', 'GO:6', 'GO:7'],
                  'A4': ['GO:1', 'GO:0', 'GO:7', 'GO:6', 'GO:2']}
    trandatata = ["B1\tA1",
                  "B2\tA2",
                  "B3\tA3",
                  "B4\tA4"]
    testdata = ["B1", "B2", "B3", "B4"]

    predictor = Predictor(trandatata, args=None)
    predictor.set_trainclass(trainclass, PLST=True)
    predictor.get_predictions(testdata, PLST=True, PLST_class=PLST)

