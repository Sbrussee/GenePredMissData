import numpy as np
class Converter:
    def __init__(self):
        self.terms_test = {}
        self.terms_unique = []
        self.array_training = np.array([])
        self.array_test = np.array([])
        self.length = 0

    # Import: the whole test data and create an array of all unique values.
    # Output: A list of all unique values, the size of the test set, and all the test terms.
    def set_terms_unique_test(self, lijst):
        self.length = len(lijst)
        self.terms_test = lijst
        array = np.array([])
        for terms in lijst.values():
            array = np.append(array, terms)
        self.terms_unique = list(np.unique(array))

    # Create a numpy array with onzly zeros for the test and training data.
    def set_np(self):
        self.array_training = np.zeros((self.length, len(self.terms_unique)))
        self.array_test = np.zeros((self.length, len(self.terms_unique)))

    # Change the zero to a one for the test set if the go term exist per protein.
    def set_test_np(self):
        getal = 0
        for id, terms in self.terms_test.items():
            for term in terms:
                index = self.terms_unique.index(term)
                self.array_test[getal, index] = 1
            getal += 1

    # Change the zero to a one for the training set if the go term exist per protein.
    # Dictionaires of the test and training are in the same order.
    # The training id must exist also in the test set.
    # If go term not in unique values, extend the numpy array of both test and training array.
    def set_training_np(self, training):
        getal = 0
        for id, terms in training.items():
            for term in terms:
                if term not in self.terms_unique:
                    nieuw = np.zeros((self.length, 1))
                    self.array_training = np.append(self.array_training, nieuw, axis=1)
                    self.array_test = np.append(self.array_test, nieuw, axis=1)
                    self.terms_unique.append(term)
                index = self.terms_unique.index(term)
                self.array_training[getal, index] = 1
            getal += 1

    # Return test and training array.
    def get_array(self):
        return self.array_test, self.array_training


if __name__ == "__main__":
    """
    1. Not all go terms comparing between the two set are in the right order, or are in both sets.
   
     Step 1: Make a list with all unique go terms from the test set.
     Step 2: Create numpy arrays for test and training set with the size of the test set
     Step 3: Test array: Change 0 to 1 for test array if go term exist for a protein id
     Step 4: Training array: Change 0 to 1 for test array if go term exist for a protein id
     Step 5: Extend the unique list with training terms if the term does not exist in the unique list.
     """

    # The set with for each term the right assignment.
    true_assignment = {
        "gen1": ["go1", "go22", "go3", "go10", "go5", "go6", "go7", "go8", "go9", "go10", "go11", "go12", "go13"],
        "gen3": ["go14", "go15", "go136", "go17", "go22", "go33", "go11", "go8", "go9", "go112", "go119", "go159", "go13"],
        "gen4": ["go1", "go2", "go35", "go4", "go45", "go56", "go755", "go11", "go99", "go10", "go11", "go12", "go133"],
        "gen5": ["go1", "go12", "go3", "go44", "go454", "go20", "go17", "go98", "go93", "go10", "go11", "go12", "go13"],
        "gen2": ["go1", "go2", "g4o3", "go4", "go5", "go6", "go7", "go8", "go9", "go10", "go3311", "go12", "go1344"]}

    # The set which will be made from the predictor and fix_go classe.
    training_assignment = {
        "gen1": ["go14", "go15", "go136", "go17", "go22", "go33", "go11", "go8", "go9333", "go112", "go119", "go159", "go3322"],
        "gen3": ["go1", "go2", "go35", "go4", "go45", "go56", "go755", "go11", "go99", "go10", "go11", "go12", "go133"],
        "gen4": ["go1", "go22", "go3", "go10", "go5", "go6", "go7", "go8", "go9", "go10", "go4411", "go12", "go13"],
        "gen5": ["go1", "go12", "go3", "go44", "go454", "go20", "go17", "go98", "go93", "go10", "go11", "go12", "gorr13"],
        "gen2": ["go1", "go2", "g4o3", "go4", "go5", "go6", "go7", "go8", "go9", "go10", "go11", "go12", "go1344"]}

    # Call class
    converter = Converter()

    # Step 1: All test/training unique terms. Training terms will be called in the fix_go loop:
    converter.set_terms_unique_test(true_assignment)
    converter.set_np()
    converter.set_test_np()

    # In de go fix loop
    converter.set_training_np(training_assignment)

    # Nadat geloopt is:
    test_array, training_array = converter.get_array()

    print(test_array)
    print()
    print(training_array)
