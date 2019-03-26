"""
Simple version of a data splitter function.
Next step is to make it work in a class.
"""

from class_splitter import Splitter
import random


def counter():
    """
    Counts the rows of the output file from the prediction class
    and returns it.
    """
    with open("mgi.gaf") as f:
        for i, l in enumerate(f):
            pass
    return i + 1
    

def main():
    """
    The main input asks the user for a percentage input.
    If the user chooses anything else than a percentage
    the input question will be asked again.
    """
    perc_input = int(input("Give the splitting percentage: "))
    while type(perc_input) != int:
        perc_input = int(input("Error: please enter a number: "))
    row_count = counter()
    splitten = Splitter(perc_input, row_count)
    splitten.splitter()


main()
