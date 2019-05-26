import numpy as np
from scipy.sparse import lil_matrix as lil
import sys
import itertools

"This class predicts only the best blast hit, whereby the used best hit is not checked if it is annotated."
class Predictor:

    """ constructor: the blast results are going to be saved in a dictionaire.
        traindata = blast results
        self.traindata = dictionaire where the blast results will be saved"""
    def __init__(self, traindata, args):
        self.traindata = {}
        for line in traindata:
            line = line.split("\t")
            if len(line) > 1:
                self.traindata[line[0]] = line[1]


    """ This function saves the gaf file from the train set(rat gaf) in a class or matrix dependent on PLST method
        1. Determine if the PLST method is used.
            - self.go_termen_train: to store all unique go terms in a list
            - self.go_index: index all the unique go terms with the go term as key
            - self.go_index_reverse: Switched key-values from self.go_index, so that index number is the key
            - self.train_id_reverse: index the protein ids with the index number as key
            - self.matrix: The matrix on the i-th row the protein ids, and the j-th row the go terms.
                a 0 indicates a go term is absent on a protein and a 1 indicates the go term is present
            - self.rat index: determines the index of the proteins used in the self.matrix
            
        2. If PLST method is not used then:
            - self.trainclass: store in a dictionaire all proteins with the specific go terms"""
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


    """ Predict the go terms for the the proteome.
        - predictions: all the predictions are stored in this dictionaire. 
        1. If the PLST method is used:
            - transformed_matrix: transform the self.matrix
            - predicted_matrix: Determine which rows of the transformed_matrix are used for the prediction
            - inverse_matrix: Convert the predicted matrix values back to normal values
            - store the go terms per protein from the inverse_matrix into a dictionaire.
        2. If the PLST method is not used:
            - determine the prediction into the not_PLST_predictions function. """
    def get_predictions(self, testdata, PLST, PLST_class, besthits=None):
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

    """Determine the bool for type of array(blast beshtit or top20 hits)"""
    def get_dtype(self):
        return bool

"""This functions determines the prediction if the PLST method is used
- index: To determine the proteins used from the transformed matrix
- protein_volgorde: list with the protein order in the predictions made
- returns the predicted matrix and the protein order"""
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

"""This function convert the self.matrix to the transformed_matrix with the PLST method.
- transform: Call the PLST class
- transformed _matrix: The matrix returned from the PLST class.
- Exit script if method gives an error
- return the transformed matrix and the PLST class to convert the transformed matrix back"""
def call_PLST_class(self, PLST_class):
    getal = int("%.0f" % (self.matrix.shape[1] / 4))
    transform = PLST_class()
    try:
        transformed_matrix = transform.fit(self.matrix, ndims=getal)
    except:
        print("plst methode werkt niet op matrix: ", self.matrix.shape)
        sys.exit()
    return transformed_matrix, transform

"""This function determines the prediction if the PLST method is not used.
- predictions: All the predictions are stored in this variable.
- returns the predictions dictionaire."""
def not_PLST_predictions(self, testdata):
    predictions = {}
    for protein in testdata:
        protein = protein.strip()
        if protein in self.traindata:
            protein_class = self.traindata[protein].strip()
            if protein_class in self.trainclass:
                predictions[protein] = self.trainclass[protein_class]
    return predictions


