import itertools
import numpy as np
import sys

"""This class can predict the best blasthit or more blast hits, whereby the used best" 
    hits are checked if they are annotated"""
class Predictor:

    """ constructor: to save the blast results in a dictionaire.
    self.traindata: dictionaire with the blast results.
    self.besthits: Specifies how many blast hits are taken.
    self.only_annotate: Specifies if only annotated proteins must be used for the prediction."""
    def __init__(self, traindata, args):
        self.traindata = {}
        self.besthits = int(args[0])
        self.only_annotate = args[1]
        self.only_annotate = self.only_annotate.lower() == 'true'
        for id in traindata:
            id = id.split("\t")
            input = id[0].strip()
            output = id[1].strip()
            if input in self.traindata:
                self.traindata[input].append(output)
            elif input not in self.traindata:
                self.traindata[input] = []
                self.traindata[input].append(output)

    """
    Function: To get the right number of blast hits for each subject.
    The results are saved in the traindata dictionaire. 
    """
    def correct_traindata(self,  rat_index):
        traindata = {}
        if self.only_annotate:
            for keys, val in self.traindata.items():
                traindata[keys] = []
                getal = 0
                for values in val:
                    if values in rat_index and getal < self.besthits:
                        getal += 1
                        traindata[keys].append(values)

        else:
            for keys, val in self.traindata.items():
                traindata[keys] = []
                getal = 0
                for values in val:
                    if getal < self.besthits:
                        getal += 1
                        traindata[keys].append(values)
        return traindata


    """
    Function: To get the matrix with the go terms of all predicted proteins.
    1. At first, the traindata needs to be corrected for the number of hits for each subject.
    index: To get the index of the predicted matrix according to the predictions.  
    rat: To save the genes in the rat in a dictionaire. 
    """
    def get_predictions(self, testdata, matrix, rat_index):
        self.traindata = self.correct_traindata(rat_index)
        self.prediction_data = {}
        index = []
        rat = {}
        getal = 0
        for protein in testdata:
            protein = protein.strip()
            if protein in self.traindata:
                if len(self.traindata[protein]) > 0:
                    for prot in self.traindata[protein]:
                        if prot not in rat:
                            if prot in rat_index:
                                index.append(rat_index[prot])
                                rat[prot] = getal
                                getal += 1
                        if prot in rat_index:
                            if protein not in self.prediction_data:
                                self.prediction_data[protein] = []
                            self.prediction_data[protein].append(prot)
                        elif prot not in rat_index and protein in self.prediction_data:
                            self.prediction_data[protein].append("not annotated")
        return matrix[index], rat


    """
    Function: Determine the type of prediction array needs to be made.
    hits > 1 == float
    anders == bool.
    """
    def get_dtype(self):
        if self.besthits > 1:
            return float
        return bool

    """
    Function to get the traindata
    """
    def get_train(self):
        return self.prediction_data








