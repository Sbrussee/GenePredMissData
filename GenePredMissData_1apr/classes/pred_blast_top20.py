import numpy as np
import itertools
class Predictor_top20:
    def __init__(self, traindata):
        self.traindata = {}
        for id in traindata:
            id = id.split("\t")
            input = id[0]
            output = id[-1].strip()
            if input in self.traindata:
                self.traindata[input].append(output)
            elif input not in self.traindata:
                self.traindata[input] = []
                self.traindata[input].append(output)

    def set_trainclass(self, trainclass):
        global train
        train = trainclass
        self.trainclass = trainclass

    # Create the prediction set
    def get_predictions(self, testdata):
        predictions = {}
        for protein in testdata:
            protein = protein.strip()
            if protein in self.traindata:
                protein_class = self.traindata[protein]
                if len(protein_class) > 1:
                    blast_extend = [self.trainclass[prot] for prot in protein_class if prot in self.trainclass]
                    blast_list = list(itertools.chain.from_iterable(blast_extend))
                    unique, counts = np.unique(blast_list, return_counts=True)
                    predictions[protein] = list(zip(unique, counts/len(blast_extend)))
        return predictions

    def get_dtype(self):
        return float


