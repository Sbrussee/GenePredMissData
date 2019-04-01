import numpy as np


class Converter:
    def __init__(self):
        self.terms_test = {}
        self.terms_unique = []
        self.array_training = np.array([])
        self.array_test = np.array([])
        self.length = 0
        self.getal=0

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
        self.array_training = np.zeros((self.length, len(self.terms_unique)), dtype="int")
        self.array_test = np.zeros((self.length, len(self.terms_unique)), dtype="int")

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
        for id, terms in training.items():
            for term in terms:
                if term not in self.terms_unique:
                    nieuw = np.zeros((self.length, 1), dtype="int")
                    self.array_training = np.append(self.array_training, nieuw, axis=1)
                    self.array_test = np.append(self.array_test, nieuw, axis=1)
                    self.terms_unique.append(term)
                index = self.terms_unique.index(term)
                self.array_training[self.getal, index] = 1
        self.getal+=1


    # Return test and training array.
    def get_array(self):
        return self.array_test, self.array_training
