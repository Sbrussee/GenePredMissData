import pandas as pd
import numpy as np

# Class predictor:
# 1. Determine predictor method, e.g. blast best hit
# 2. Get the train data for the used method.
# 3. get the train gaf file.
# 4. Extend the go-terms for the train data
# 5. If blast method > 1 best hit then calculate frequence.


# Part 1: the predictor method.
class Predictor:
    # Import the train data and get all blast results for the best blast hit or blast extension.
    # Temporary extend: Can be changed to predictor method.
    def __init__(self, traindata, extend):
        self.extend = extend
        if self.extend == 1:
            self.traindata = get_lijst_no_extend(self, traindata)
        else:
            self.traindata = get_lijst_extend(self, traindata, extend)


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



# Part 2: Functions depending on blast method in predictor.


# Get traindata if the best blast hit score is 1
# self.traindata = traindata
def get_lijst_no_extend(self, traindata):
    self.traindata = {}
    for line in traindata:
        line = line.split("\t")
        if len(line) > 1:
            self.traindata[line[0]] = line[1].strip()
    return self.traindata

# Get traindata if the best blast hit score is > 1
# self.traindata = traindata
def get_lijst_extend(self, traindata, extend):
    self.traindata = {}
    remember, count = "", 0
    for line in traindata:
        if line.strip() != "":
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
    return self.traindata


# Get prediction if blast extension
# Prediction = id + go termen + frequence per go term
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
# Prediction is id + go termen   (without frequence)
def get_blast(clas, train, test):
    predictions = {}
    for protein in test:
        protein = protein.strip()
        if protein in train:
            protein_class = train[protein]
            if protein_class in clas:
                predictions[protein] = clas[protein_class]
            else:
                predictions[protein] = []
        else:
            predictions[protein] = []
    return predictions




# Part 3: Classe to calculate frequence if blast hit > 1:


# If blast extension calculate the precision for each protein.
# 1. save all predicted ids for each true protein
# 2. Return frequentie list per predicter protein per true protein.
class extend_converter:
    def __init__(self):
        self.blast_extend = []
        self.count = 0

    # Save uniprot id in temporary list new.
    def get_blast_extend(self, blast_extend):
        self.blast_extend.append(blast_extend)
        self.count += 1

    # Calculate frequence go terms for als go terms per true in in temporary list new.
    # Use pandas to set all go terms in list and calculate values.
    def set_blast_extend(self):
        array = np.array([])
        for lines in self.blast_extend:
            for regels in lines:
                array = np.append(array, regels)

        check = pd.DataFrame({'a': array})
        frame = check['a'].sort_values().value_counts() / self.count
        self.count = 0
        return list(zip(frame.index, frame.values))
