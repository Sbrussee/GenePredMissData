import random

class Splitter:
    def __init__(self, fraction, input_file):
        self.fraction = fraction
        self.input_file = input_file

    def splitter(self):
        """
        Depending on the percentage and the amount of lines in the file
        it will split the data and saves the test data into a seperate file.
        """
        opslag = {}
        for id, term in self.input_file.items():
            sample_size = len(term) * self.fraction // 100
            sample = random.sample(term, int(sample_size))
            opslag[id] = sample
        return opslag