import pandas as pd
import numpy as np
class Predictor:
    # Import the train data and get all blast results for the best blast hit or blast extension.
    def __init__(self, traindata):
        self.blast_extend = False
        self.traindata = {}
        remember, count = "", 0
        for line in traindata:
            id = line.split("\t")
            input = id[0]
            output = id[-1].strip()
            if input == remember and count <= 20 and output not in out:
                self.blast_extend = True
                self.traindata[input].append(output)
                count += 1
            elif input != remember:
                out = []
                out.append(output)
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
        if not self.blast_extend:
            prediction = get_blast(self.trainclass, self.traindata, testdata)
        if self.blast_extend:
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

    def get_blast_extend(self, blast_extend):
        self.blast_extend.append(blast_extend)

    def set_blast_extend(self):
        array = np.array([])
        length = len(self.blast_extend)
        for lines in self.blast_extend:
            array = np.append(array, lines)

        check = pd.DataFrame({'a': array})
        frame = check['a'].value_counts() / length
        return list(zip(frame.index, frame.values))
