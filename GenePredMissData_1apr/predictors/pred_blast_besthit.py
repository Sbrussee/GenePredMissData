import numpy as np
from scipy.sparse import lil_matrix as lil

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
    def set_trainclass(self, trainclass, x_pos, y_pos, PLST):
        self.y_pos = y_pos
        if PLST:
            self.matrix = np.zeros((len(y_pos), len(x_pos)))
            for lines in trainclass:
                for value in lines[1]:
                    if not lines in y_pos:
                        continue
                    if not value in x_pos:
                        continue
                    self.matrix[y_pos[lines], x_pos[value]] = 1
        else:
            global train
            train = trainclass
            self.trainclass = trainclass


    # The testdata must be imported.
    # First, the loop will look if the id from the testdata is in the blast results dictionaire: self.traindata.
    # Second, the loop will look if the linked train id to the test id can be linked to the train gaf file.
    # Third, if so save the data.
    def get_predictions(self, testdata, PLST, PLST_class):
        if PLST:
            transformed_matrix, transform = call_PLST_class(self, PLST_class)
            predicted_matrix = PLST_predictions(self, testdata, transformed_matrix)
            inverse_matrix = transform.inverseMap(predicted_matrix)
            return lil(inverse_matrix)

        else:
            predictions = not_PLST_predictions(self, testdata)
            return predictions


    # If this method is used, return a bool for defining which type of array has to be made.
    def get_dtype(self):
        return bool

# Predictions if PLST
def PLST_predictions(self, testdata, transformed):
    index = []
    for protein in testdata:
        protein = protein.strip()
        if protein in self.traindata:
            if protein in self.y_pos:
                index.append(self.y_pos[protein])
    return transformed[index, :]

# Call PLST class
def call_PLST_class(self, PLST_class):
    getal = int("%.0f" % (len(self.matrix) / 4))
    transform = PLST_class()
    transformed_matrix = transform.fit(self.matrix, ndims=getal)
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
