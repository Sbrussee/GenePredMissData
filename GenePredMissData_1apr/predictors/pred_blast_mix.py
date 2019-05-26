import itertools
import numpy as np
import sys
# This predictor calls all the results from the blast hit
class Predictor:

    # The traindata must be imported to save all the blast results in the dictionaire self.traindata.
    def __init__(self, traindata, args):
        self.traindata = {}
        for id in traindata:
            id = id.split("\t")
            input = id[0].strip()
            output = id[1].strip()
            if input in self.traindata:
                self.traindata[input].append(output)
            elif input not in self.traindata:
                self.traindata[input] = []
                self.traindata[input].append(output)

    # This function imports the train gaf file(rat gaf)
    def set_trainclass(self, trainclass, PLST):
        if PLST:
            # Step 1: Determine how big the matrix will be.
            self.go_termen_train = [go for go in trainclass.values()]
            self.go_termen_train = list(itertools.chain.from_iterable(self.go_termen_train))
            self.go_termen_train = np.unique(self.go_termen_train)
            self.go_index = {a: getal for getal, a in enumerate(np.unique(self.go_termen_train))}
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
    def get_predictions(self, testdata, PLST, PLST_class, besthits=1):
        self.besthits = besthits
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
            self.traindata = determine_annotated_data(self)
            predictions = not_PLST_predictions(self, testdata)
        return predictions


    def get_dtype(self):
        return bool

def determine_annotated_data(self):
    traindata = {}
    for keys in self.traindata:
        traindata[keys] = []
        getal = 0
        for values in self.traindata[keys]:
            if values in self.trainclass and getal < self.besthits:
                getal += 1
                traindata[keys].append(values)
    return traindata

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
        protein_class = []
        if protein in self.traindata:
            protein_class = self.traindata[protein]

        if len(protein_class) == 1 and self.besthits == 1:
            predictions[protein] =  self.trainclass[protein_class[0]]
        if len(protein_class) > 0 and self.besthits > 1:
            # Here, the frequency will be calculated:
            blast_extend = [self.trainclass[prot] for prot in protein_class if prot in self.trainclass]
            blast_list = list(itertools.chain.from_iterable(blast_extend))
            unique, counts = np.unique(blast_list, return_counts=True)
            predictions[protein] = list(zip(unique, counts / len(blast_extend)))

    return predictions