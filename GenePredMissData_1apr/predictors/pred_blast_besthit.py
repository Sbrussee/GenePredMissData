# This class is to predict if only the blast besthit method is used.
class Predictor:

    # Traindata must be imported and the blast results will be saved into the traindata dictionaire.
    def __init__(self, traindata):
        self.traindata = {}
        for line in traindata:
            line = line.split("\t")
            if len(line) > 1:
                self.traindata[line[0]] = line[1]

    # This function saves the gaf file from the train set(rat gaf)
    def set_trainclass(self, trainclass):
        global train
        train = trainclass
        self.trainclass = trainclass

    # The testdata must be imported.
    # First, the loop will look if the id from the testdata is in the blast results dictionaire: self.traindata.
    # Second, the loop will look if the linked train id to the test id can be linked to the train gaf file.
    # Third, if so save the data.
    def get_predictions(self, testdata):
        predictions = {}
        for protein in testdata:
            protein = protein.strip()
            if protein in self.traindata:
                protein_class = self.traindata[protein].strip()
                if protein_class in self.trainclass:
                    predictions[protein] = self.trainclass[protein_class]
        return predictions

    # If this method is used, return a bool for defining which type of array has to be made.
    def get_dtype(self):
        return bool
