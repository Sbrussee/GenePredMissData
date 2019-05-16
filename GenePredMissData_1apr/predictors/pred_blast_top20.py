import numpy as np
import itertools

# This method will be used if the top 20 best blast hits must be predicted.
class Predictor:

    # The traindata must be imported to save the blast results in the dictionaire self.traindata.
    def __init__(self, traindata, args):
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
        print("train data:", self.traindata)

    # This function imports the train gaf file(rat gaf)
    def set_trainclass(self, trainclass, PLST):
        global train
        train = trainclass
        self.trainclass = trainclass
        print("self.trainclass", self.trainclass)

    # This functions looks if the test ids can be linked to the train gaf.
    # First, the loop will look if the id from the testdata is in the blast results dictionaire: self.traindata.
    # Second, the loop will look if the linked train id to the test id can be linked to the train gaf file.
    # Third, if so calculate the frequency each go-term exist in a train protein id.
    # Because there are 20 train ids and only 1 test id, therefore the frequency will be calculated.
    # Fourth, save the frequency in the dictionaire: predictions.
    def get_predictions(self, testdata, PLST, PLST_class):
        predictions = {}
        for protein in testdata:
            protein = protein.strip()
            if protein in self.traindata:
                protein_class = self.traindata[protein]
                if len(protein_class) > 1:

                    # Here, the frequency will be calculated:
                    blast_extend = [self.trainclass[prot] for prot in protein_class if prot in self.trainclass]
                    blast_list = list(itertools.chain.from_iterable(blast_extend))
                    unique, counts = np.unique(blast_list, return_counts=True)
                    predictions[protein] = list(zip(unique, counts/len(blast_extend)))

        print("Predictions:", predictions)
        return predictions

    # If this method is used, return a float for defining which type of array has to be made.
    def get_dtype(self):
        return float


# Werkt het script?
if __name__ == "__main__":
    traindata = ['A1\tB1', 'A1\tB2', "A1\tB3",
                 'A2\tB4', 'A2\tB5', "A2\tB6",
                 'A3\tB7', 'A3\tB8', "A3\tB9"]
    trainclass = {"B1":["GO1", "GO2", "GO3"],
                  "B2":["GO1", "GO2", "GO3"],
                  "B3":["GO1", "GO2", "GO3"],
                  "B4":["GO1", "GO2", "GO3"],
                  "B5":["GO4", "GO5", "GO6"],
                  "B6":["GO1", "GO2", "GO3"],
                  "B7":["GO1", "GO2", "GO3"],
                  "B8":["GO4", "GO5", "GO6"],
                  "B9":["GO7", "GO8", "GO9"],}
    testdata=['A1', "A2", "A3"]
    predictor = Predictor(traindata, args=None)
    predictor.set_trainclass(trainclass, PLST=None)
    predictor.get_predictions(testdata, PLST=None, PLST_class=None)

