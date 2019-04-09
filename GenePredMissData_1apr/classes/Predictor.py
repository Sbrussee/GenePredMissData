import pandas as pd
import numpy as np

# Class predictor:
# 1. Determine predictor method, e.g. blast best hit
# 2. Get the train data for the used method.
# 3. get the train gaf file.
# 4. Extend the go-terms for the train data
# 5. If blast method > 1 best hit then calculate frequence.



class Predictor:
    # Import the train data and get all blast results for the best blast hit or blast extension.
    # Temporary extend: Can be changed to predictor method.
    def __init__(self, traindata, extend):
        # Call the blast method classe
        self.blast = blast_method()

        # extend is temporary to define the blast method
        self.extend = extend
        if extend > 0:
            self.traindata = self.blast.get_blast_data(traindata)

    # Import the train gaf file.
    def set_trainclass(self, trainclass):
        self.trainclass = trainclass

    # Get prediction for or blast extension or best blast hit.
    def get_predictions(self, testdata):
        if self.extend > 0:
            prediction = self.blast.get_prediction(self.trainclass, self.traindata, testdata)
        return prediction



# De static functions to create the blast method
class blast_method:
    # Get the blast results
    @staticmethod
    def get_blast_data(traindata):
        train = {}
        for id in traindata:
            id = id.split("\t")
            input = id[0]
            output = id[-1].strip()
            if input in train:
                train[input].append(output)
            elif input not in train:
                train[input] = []
                train[input].append(output)
        return train

    # Create the prediction set
    @staticmethod
    def get_prediction(trainclas, traindata, testdata):
        predictions = {}
        for protein in testdata:
            protein = protein.strip()
            if protein in traindata:
                protein_class = traindata[protein]
                if len(protein_class) > 1:
                    extend = extend_converter()
                    for prot in protein_class:
                        if prot in trainclas:
                            extend.get_blast_extend(trainclas[prot])
                    predictions[protein] = extend.set_blast_extend()

                else:
                    protein_class = protein_class[0]
                    if protein_class in trainclas:
                        predictions[protein] = trainclas[protein_class]
        return predictions



# If blast extension calculate the precision for each protein.
# 1. save all predicted ids for each true protein
# 2. Return frequentie list per predicter protein per true protein.
class extend_converter:
    def __init__(self):
        self.blast_extend = np.array([])
        self.count = 0

    # Save uniprot id in temporary list new.
    def get_blast_extend(self, blast_extend):
        new = []
        if len(blast_extend) > 1:
            for regel in blast_extend:
                if regel not in new:
                    new.append(regel)
                    self.blast_extend = np.append(self.blast_extend, regel)
        else:
            self.blast_extend = np.append(self.blast_extend, blast_extend)
        self.count += 1

    # Calculate frequence go terms for als go terms per true in in temporary list new.
    # Use pandas to set all go terms in list and calculate values.
    def set_blast_extend(self):
        check = pd.DataFrame({'a': self.blast_extend})
        frame = check['a'].sort_values().value_counts() / self.count
        self.count = 0
        return list(zip(frame.index, frame.values))
