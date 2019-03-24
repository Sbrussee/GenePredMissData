import numpy as np
class Converter:
    def __init__(self):
        self.terms_unique = []
        self.total_protein = []
        self.length = 0
        self.rows = 0
        self.array_training = np.array([])
        self.array_test = np.array([])
        self.test_ids = {}
        self.training_id = {}
        self.test_volgorde = []

    def get_terms_unique(self, lijst):
        for id, terms in lijst.items():
            for term in terms:
                if term not in self.terms_unique:
                    self.terms_unique.append(term)
            if id not in self.total_protein:
                self.total_protein.append(id)

    def get_test_terms(self, test):
        self.test_ids = test

    def get_training_terms(self, training):
        self.training_id.update(training)

    def set_np(self):
        self.array_training = np.zeros((len(self.total_protein), len(self.terms_unique)), dtype='int')
        self.array_test = np.zeros((len(self.total_protein), len(self.terms_unique)), dtype='int')

    def set_test_np(self):
        getal = 0
        for id, terms in self.test_ids.items():
            self.test_volgorde.append(id)
            for term in terms:
                index = self.terms_unique.index(term)
                self.array_test[getal, index] = 1
            getal += 1
        return self.array_test

    def set_training_np(self):
        for id, terms in self.training_id.items():
            getal = self.test_volgorde.index(id)
            for term in terms:
                index = self.terms_unique.index(term)
                self.array_training[getal, index] = 1
        return self.array_training

if __name__ == "__main__":
    """
    1. Probably the dictionaire keys between training en test data are unoredered in the dictionaire.
    2. Not all go terms comparing between the two set are in the right order, or are in both sets.
    4. if the size between training/test set are not identical, the numpy array has the size of the longest possibly.
   
     Step 1: Make a list with all unique go terms for the training set.
     Step 2: Extend the unique list with training terms if the term does not exist in the unique list.
     Step 3: - Create a numpy array with the len of unique list and rows with the len of the set with the most rows.
             - So, check for each term in the list in which column the go-term in the header is located. 
             - if term exist 1, otherwise 0. 
    Step 4: - Create a numpy array with help of the test set, because all ids must be placed on the same row. 
            - if term exist 1, otherwise 0. 
     """

    # The set with for each term the right assignment.
    true_assignment = {
        "gen1": ["go1", "go22", "go13", "go10", "go5", "go6", "go7", "go8", "go9", "go10", "go11", "go12", "go13"],
        "gen3": ["go14", "go15", "go136", "go17", "go22", "go33", "go11", "go8", "go9", "go112", "go119", "go159", "go13"],
        "gen4": ["go1", "go2", "go35", "go4", "go45", "go56", "go755", "go11", "go99", "go10", "go11", "go12", "go133"],
        "gen5": ["go1", "go12", "go3", "go44", "go454", "go20", "go17", "go98", "go93", "go10", "go11", "go12", "go13"],
        "gen2": ["go1", "go2", "g4o3", "go4", "go5", "go6", "go7", "go8", "go9", "go10", "go11", "go12", "go1344"]}

    # The set which will be made from the predictor and fix_go classe.
    training_assignment = {
        "gen3": ["go11", "go2", "go1", "go10", "go51", "go62", "go37", "go8", "go94", "go10", "go11", "go12", "go13"],
        "gen4": ["go14", "go15", "go136", "go1", "go222", "go332", "go131", "go84", "go91", "go112", "go11", "go15", "go13"],
        "gen1": ["go1", "go2", "go35", "go4", "go45", "go56", "go11", "go99", "go10", "go11", "go12", "go133"],
        "gen5": ["go1", "go12", "go3", "go44", "go454", "go20", "go17", "go12", "go13"],
        "gen2": ["go1", "go23", "go43", "go25", "go16", "go17", "go8", "go9", "go10", "go11", "go12", "go1344"]}

    # Call class
    converter = Converter()

    # Step 1: All test/training unique terms. Training terms will be called in the fixx_go loop:
    converter.get_terms_unique(true_assignment)
    converter.get_test_terms(true_assignment)

    converter.get_terms_unique(training_assignment)
    converter.get_training_terms(training_assignment)

    # Step 3: After fix_go loop is finished, get np.array with right size filled with zeros.
    converter.set_np()

    # Step 4: Create test and training vectorizes, whereby the zero in the array change to a 1 for each term.
    test_array = converter.set_test_np()
    training_array = converter.set_training_np()

    print(test_array)
    print()
    print(training_array)
