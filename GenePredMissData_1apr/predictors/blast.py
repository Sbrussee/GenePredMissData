import itertools
import numpy as np
import sys

"""This class can predict the best blasthit or more blast hits, whereby the used best" 
    hits are checked if they are annotated"""
class Predictor:

    """ constructor: the blast results are going to be saved in a dictionaire.
        traindata = blast results
        self.traindata = dictionaire where the blast results will be saved"""
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


    def correct_traindata(self,  rat_index):
        traindata = {}
        for keys in self.traindata:
            traindata[keys] = []
            getal = 0
            for values in self.traindata[keys]:
                if self.only_annotate:
                    if values in rat_index and getal < self.besthits:
                        getal += 1
                        traindata[keys].append(values)
                else:
                    if getal < self.besthits:
                        getal += 1
                        traindata[keys].append(values)
        return traindata


    """This function determines the prediction if the PLST method is not used.
    - predictions: All the predictions are stored in this variable.
    - returns the predictions dictionaire
    - self.besthits: specifies the hits used for the blast."""
    def get_predictions(self, testdata, matrix, rat_index):
        self.traindata = self.correct_traindata(rat_index)
        index = []
        rat = {}
        getal = 0
        for protein in testdata:
            protein = protein.strip()
            if protein in self.traindata:
                protein_class = self.traindata[protein]
                for prot in protein_class:
                    if prot not in rat:
                        rat[prot] = getal
                        if prot in rat_index:
                            index.append(rat_index[prot])
                            getal += 1
        return matrix[index], rat


    """Determine the bool for type of array(blast beshtit or top20 hits)"""
    def get_dtype(self):
        if self.besthits > 1:
            return float
        return bool

    def get_train(self):
        return self.traindata








