"""
Simple version of a data splitter function.
Next step is to make it work in a class.
"""

from klasse_splitter import Splitter
import random


def counter():
    """
    Counts the rows of the output file from the prediction class
    and returns it.
    """
    with open("output_file.txt") as f:
        for i, l in enumerate(f):
            pass
    return i + 1
    

def main():
    """
    The main input asks the user for a percentage input.
    For now the program only works with 10, 25, or 50.
    If the user chooses anything else than these options
    the input question will be asked again.
    """
    perc_input = int(input("Give the splitting percentage: "))
    while perc_input not in [10, 25, 50]:
        perc_input = int(input("Error: please enter 10, 25, or 50: "))
    row_count = counter()
    splitten = Splitter(perc_input, row_count)
    splitten.splitter()


main()
