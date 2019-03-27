import random

class Splitter:
    def __init__(self, fraction, input_file):
        self.fraction = fraction
        self.file_length = sum(1 for line in input_file)
        self.input_file = input_file

    def splitter(self):
        """
        Depending on the percentage and the amount of lines in the file
        it will split the data and saves the test data into a seperate file.
        """
        sample_size = self.file_length * self.fraction // 100
        sample = random.sample(self.input_file, sample_size)
        return sample

    




