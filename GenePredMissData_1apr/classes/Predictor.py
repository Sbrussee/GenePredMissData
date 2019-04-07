import pandas as pd
import numpy as np
class Predictor:
    # Import the train data and get all blast results for the best blast hit or blast extension.
    def __init__(self, traindata, extend):
        self.extend = extend
        self.traindata = {}
        remember, count = "", 0
        for line in traindata:
            id = line.split("\t")
            input = id[0].strip()
            output = id[-1].strip()
            if input == remember and count < extend:
                self.traindata[input].append(output)
                count += 1
            elif input != remember:
                remember = input
                self.traindata[input] = []
                self.traindata[input].append(output)
                count = 1


    # Import the train gaf file.
    def set_trainclass(self, trainclass):
        global train
        train = trainclass
        self.trainclass = trainclass

    # Get prediction for or blast extension or best blast hit.
    def get_predictions(self, testdata):
        prediction = {}
        if self.extend == 1:
            prediction = get_blast(self.trainclass, self.traindata, testdata)
        if self.extend > 1:
            prediction = get_blast_extend(self.trainclass, self.traindata, testdata)
        return prediction

# Get prediction if blast extension
def get_blast_extend(clas, train, test):
    predictions = {}
    for protein in test:
        doorgaan = False
        protein = protein.strip()
        if protein in train:
            protein_class = train[protein]
            extend = extend_converter()
            for prot in protein_class:
                if prot in clas:
                    extend.get_blast_extend(clas[prot])
                    doorgaan = True

            if doorgaan:
                predictions[protein] = extend.set_blast_extend()
    return predictions

# get prediction if no blast extension
def get_blast(clas, train, test):
    predictions = {}
    for protein in test:
        protein = protein.strip()
        if protein in train:
            protein_class = train[protein][0]
            if protein_class in clas:
                predictions[protein] = clas[protein_class]
            else:
                predictions[protein] = []
        else:
            predictions[protein] = []
    return predictions


# If blast extension calculate the precision for each protein.
class extend_converter:
    def __init__(self):
        self.blast_extend = []
        self.count = 0

    def get_blast_extend(self, blast_extend):
        new = []
        if len(blast_extend) > 1:
            for regels in blast_extend:
                if regels not in new:
                    new.append(regels)
            self.blast_extend.append(new)
        else:
            self.blast_extend.append(blast_extend)
        self.count += 1

    def set_blast_extend(self):
        array = np.array([])
        for lines in self.blast_extend:
            for regels in lines:
                array = np.append(array, regels)

        check = pd.DataFrame({'a': array})
        frame = check['a'].sort_values().value_counts() / self.count
        self.count = 0
        return list(zip(frame.index, frame.values))
