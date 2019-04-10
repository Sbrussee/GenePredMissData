import numpy as np
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
                    extend = extend_converter()
                    for prot in protein_class:
                        if prot in self.trainclass:
                            extend.get_blast_extend(self.trainclass[prot])
                    predictions[protein] = extend.set_blast_extend()
                else:
                    protein_class = protein_class[0]
                    if protein_class in self.trainclass:
                        predictions[protein] = self.trainclass[protein_class]
        return predictions

    def get_dtype(self):
        return float


# If blast extension calculate the precision for each protein.
# 1. save all predicted ids for each true protein
# 2. Return frequentie list per predicter protein per true protein.
class extend_converter:
    def __init__(self):
        self.count = 0
        self.blast_extend = np.array([])

    # Save uniprot id in temporary list new.
    def get_blast_extend(self, blast_extend):
        self.blast_extend = np.append(blast_extend, blast_extend)
        self.count += 1

    # Calculate frequence go terms for als go terms per true in in temporary list new.
    # Use pandas to set all go terms in list and calculate values.
    def set_blast_extend(self):
        self.blast_extend = np.unique(self.blast_extend)
        unique, counts = np.unique(self.blast_extend, return_counts=True)
        counts = counts / self.count
        self.count = 0
        return list(zip(unique, counts))
