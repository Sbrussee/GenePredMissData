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
        print("cool", args)
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
    def set_trainclass(self, trainclass, besthits):
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
    def get_predictions(self, testdata):
        predictions = {}
        for protein in testdata:
            protein = protein.strip()
            if protein in self.traindata:
                protein_class = self.traindata[protein].strip()
                if protein_class in self.trainclass:
                    predictions[protein] = self.trainclass[protein_class]
        return predictions

    """Determine the bool for type of array(blast beshtit or top20 hits)"""
    def get_dtype(self):
        return bool

    def get_train(self):
        return self.traindata





