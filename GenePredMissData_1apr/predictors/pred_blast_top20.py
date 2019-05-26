import numpy as np
import itertools

"This class predicts the top20 blast hits, whereby the used best hits are not checked if it is annotated."
class Predictor:

    """ constructor: the blast results are going to be saved in a dictionaire.
        traindata = blast results
        self.traindata = dictionaire where the blast results will be saved"""
    def __init__(self, traindata, args):
        self.traindata = {}
        getal = 1
        for id in traindata:
            id = id.split("\t")
            input = id[0]
            output = id[-1].strip()
            if input in self.traindata and getal < 20:
                getal += 1
                self.traindata[input].append(output)
            elif input not in self.traindata:
                getal = 1
                self.traindata[input] = []
                self.traindata[input].append(output)
    

    "This function stores all the annotated proteins from the train organism into the trainclass"
    def set_trainclass(self, trainclass, PLST):
        global train
        train = trainclass
        self.trainclass = trainclass
  

    """This functions looks if the test ids can be linked to the train gaf.
     1. predictions: All the predictions made are stored in this variable.
     2. iterate over the testdata to transfer the go terms from the train data for the right protein.
     3. Calculate the frequency of how often a go term is linked to a protein for the top 20 blast hit."""
    def get_predictions(self, testdata, PLST, PLST_class, besthits=None):
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

       
        return predictions

    """Determine the bool for type of array(blast beshtit or top20 hits)"""
    def get_dtype(self):
        return float
