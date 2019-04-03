class Predictor:
    def __init__(self, traindata):
        self.traindata = {}
        for line in traindata:
            line = line.split("\t")
            if len(line) > 1:
                self.traindata[line[0]] = line[1]

    def set_trainclass(self, trainclass):
        global train
        train = trainclass
        self.trainclass = trainclass


    def get_predictions(self, testdata):
        predictions = {}
        for protein in testdata:
            protein = protein.strip()
            if protein in self.traindata:
                protein_class = self.traindata[protein].strip()
                if protein_class in self.trainclass:
                    predictions[protein] = self.trainclass[protein_class]
                #else:
                    #print("PROTEIN_CLASS not in trainclass", protein_class)
                    #predictions[protein] = []
            else:
                print("PROTEIN NOT IN traindata", protein)
                predictions[protein] = []
        return predictions
        
        
        
        
