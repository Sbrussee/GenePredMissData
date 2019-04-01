import random


def split(lines, size):
    """
    Depending on the percentage and the amount of lines in the file
    it will split the data and saves the test data into a seperate file.
    """
    return random.sample(lines, int(len(lines) * (size / 100)))
