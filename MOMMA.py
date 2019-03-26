#!/usr/bin/env python3
import importlib
import random
from arguments import get_args
import time

import numpy as np
import matplotlib as mpl

from fix_go import fix_go
from fix_go import read_go_tree
from true_ann_parser import parse_true_annotation
from Evaluator import Evaluator
from Plotter import Plotter
from klasse_avaluator import Converter
from class_splitter import Splitter

def main():
    #READ THE INPUT FILES
    mouse_gaf = open("mouse.gaf", "r")
    rat_gaf = open("rat.gaf", "r")
    mouse_annotation = mouse_gaf.readlines()
    rat_annotation = rat_gaf.readlines()

    print("Loaded input files.")

    #GET THE ARGUMENTS:

    #argstore = get_args()

    #example: check missing data on 5 points (100%, 80%, 60%, 40%, 20%)
    fractions = [0, 20, 40, 60, 80, 100]

    #splice the data in 5 files with different fractions missing:
    #Using the indexing method:
    """
    dex = index_gaf("mouse.gaf", ["ND", "ISO", "IMP", "IDA", "EXP"])
    for frac in fractions:
        print(frac)
        slice_gaf("mouse.gaf", "mouse_" + str(frac) + ".gaf", dex, frac)
        print("done")
    """

    #Using the original splicing method:
    #Get line count for mouse file:
    file_length = sum(1 for line in mouse_gaf)
    for frac in fractions:
        print(frac)
        split = Splitter(frac, file_length, 'mouse.gaf', "mouse_" + str(frac) + ".gaf")
        split.splitter()
        print("Done")

    print("Fractionized data")

    #SAMPLE CODE PREDICTOR:
    #example: We want to predict 10 times for each fraction
    num_of_pred_per_frac = 10
    #for frac in fractions:
    #    for times in range(0, num_of_pred_per_frac):
    #        pred = Predictor(method)
    #        results = Predictor.predict()

    print("Retrieved prediction")

    #BECAUSE THERE IS NO PREDICTOR YET:
    #Make dictionary of sample prediction file
    #test_predictions = open("UniprotKBandGOID.txt", 'r')
    #prediction_dict = dict()
    #for line in test_predictions:
    #    line_items = line.split(" ")
    #    if line_items[0] not in prediction_dict.keys():
    #        prediction_dict[line_items[0]] = []
    #    prediction_dict[line_items[0]].append(line_items[1].rstrip("\n"))

    #Or, in order to get a more vast test set, use the parse_true_annotation function
    #to provide a 'prediction'-set based on the mouse.gaf file.
    mouse_dict = parse_true_annotation(mouse_annotation)

    #GET PARSED TRUE ANNOTATION:
    rat_dict = parse_true_annotation(rat_annotation)
    print("Parsed input data.")

    #CLOSE THE INPUT FILES
    mouse_gaf.close()
    rat_gaf.close()

    print("Closed input files.")

    #FIX THE TEST FILE:
    #doesnt work yet because there are no actual go-terms in the test data...
    go_tree = read_go_tree("go-basic.obo")
    for prot_key in rat_dict.keys():
        rat_dict[prot_key] = fix_go(rat_dict[prot_key], go_tree)

    print("Fixed tree of true annotation.")

    #FIX THE PREDICTOR OUTPUT:
    for prot_key in mouse_dict.keys():
        mouse_dict[prot_key] = fix_go(mouse_dict[prot_key], go_tree)

    print("Fixed tree of predicted annotation")

    #VECTORIZE THE TEST AND PREDICTION FILES
    # Call class
    converter = Converter()
    # Step 1: All test/training unique terms. Training terms will be called in the fixx_go loop:
    converter.get_terms_unique(rat_dict)
    converter.get_test_terms(rat_dict)

    converter.get_terms_unique(mouse_dict)
    converter.get_training_terms(mouse_dict)
    # Step 3: After fix_go loop is finished, get np.array with right size filled with zeros.
    converter.set_np()
    # Step 4: Create test and training vectorizes, whereby the zero in the array change to a 1 for each term.
    true_array = converter.set_test_np()
    prediction_array = converter.set_training_np()

    print("Vectorized true- and predicted annotation.")

    #EVALUATE THE PREDICTIONS
    evalutation = Evaluator(true_array, prediction_array)
    f1_scores = evalutation.get_f1()
    print("Average f1:", f1_scores.mean())
    print("Evaluated prediction method.")

    #PLOT THE EVALUATIONS

main()
