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
        for id in traindata:
            id = id.split("\t")
            input = id[0].strip()
            output = id[1].strip()
            if input in self.traindata:
                self.traindata[input].append(output)
            elif input not in self.traindata:
                self.traindata[input] = []
                self.traindata[input].append(output)


    def set_trainclass(self, trainclass, besthits):
        self.trainclass = trainclass
        self.besthits = besthits
        self.traindata = self.determine_annotated_data()

    """This function determines the prediction if the PLST method is not used.
    - predictions: All the predictions are stored in this variable.
    - returns the predictions dictionaire
    - self.besthits: specifies the hits used for the blast."""
    def get_predictions(self, testdata):
        predictions = {}
        for protein in testdata:
            protein = protein.strip()
            protein_class = []
            if protein in self.traindata:
                protein_class = self.traindata[protein]
            if len(protein_class) == 1 and self.besthits == 1:
                predictions[protein] = self.trainclass[protein_class[0]]
            if len(protein_class) > 0 and self.besthits > 1:
                # Here, the frequency will be calculated:
                blast_extend = [self.trainclass[prot] for prot in protein_class if prot in self.trainclass]
                blast_list = list(itertools.chain.from_iterable(blast_extend))
                unique, counts = np.unique(blast_list, return_counts=True)
                predictions[protein] = list(zip(unique, counts / len(blast_extend)))
        return predictions


    """Determine the bool for type of array(blast beshtit or top20 hits)"""
    def get_dtype(self):
        return bool

    """This function determines the annotated data
    - traindata: Dicitionaire where the annotated data will be stored
    - returns the traindata
    - self.besthit: Determines the used hits for the blast"""
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

    def get_train(self):
        return self.traindata






