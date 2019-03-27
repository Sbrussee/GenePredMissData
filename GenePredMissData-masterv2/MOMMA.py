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
from Predictorfile import Predictor


def main():
    #READ THE INPUT FILES
    mouse_gaf = open("goa_mouse.gaf", "r")
    rat_gaf = open("goa_rat.gaf", "r")
    openit = open('Refseqtouniprotkb.txt', 'r')
    mouse_annotation = mouse_gaf.readlines()
    rat_annotation = rat_gaf.readlines()
    files = openit.readlines()
    print("Loaded input files.")

    # Get uniprotKB column
    while True:
        question = input('In which column are the uniprotKB codes:')
        if question.isdigit() == True:
            break

    # Mouse or rat
    nameanimal = rat_annotation
    actualname = 'rat_'
    while True:
        whichanimal = input('Mouse or Rat:')
        if whichanimal.lower() == 'mouse':
            nameanimal = mouse_annotation
            actualname = 'mouse_'
            break
        elif whichanimal.lower() == 'rat':
            break
        else:
            print('That\'s not a mouse or rat')

    # Create a list containing only uniprotKB codes (removing for example accession codes)
    # openit is Refseqtouniprotkb.txt file
    test = [x.strip().split(" ") for x in files]
    newlist = []
    for value in test:
        newlist.append(value[int(question) - 1])
    # Call class
    predictor = Predictor()


    #example: check missing data on 5 points (100%, 80%, 60%, 40%, 20%)
    fractions = [20, 40, 60, 80, 100]

    #splice the data in 5 files with different fractions missing:
    #Using the indexing method:
    """
    dex = index_gaf("mouse.gaf", ["ND", "ISO", "IMP", "IDA", "EXP"])
    for frac in fractions:
        print(frac)
        slice_gaf("mouse.gaf", "mouse_" + str(frac) + ".gaf", dex, frac)
        print("done")
    """
    # GET PARSED TRUE ANNOTATION:
    rat_dict = parse_true_annotation(rat_annotation)
    print("Parsed input data.")

    go_tree = read_go_tree("go-basic.obo")

    #Using the original splicing method:
    #Get line count for mouse file:
    #    for prot_key in rat_dict.keys():
    #    rat_dict[prot_key] = fix_go(rat_dict[prot_key], go_tree)
    # GET THE ARGUMENTS:
    predictor.makelist(newlist)
    file_length = sum(1 for line in nameanimal)
    for frac in fractions:
        Splitter(frac, file_length, nameanimal, actualname + str(frac) + ".gaf").splitter()
        nameforpredictor = str(actualname) + str(frac) + ".gaf"
        go_iddictionary = predictor.blastgo(nameforpredictor)
        print(go_iddictionary)
        #print(go_iddictionary)
        #for key in pred:
        #    pred[key] = fix_go(rat_dict[prot_key], go_tree)


    print("Fractionized data")

    #Or, in order to get a more vast test set, use the parse_true_annotation function
    #to provide a 'prediction'-set based on the mouse.gaf file.
    mouse_dict = parse_true_annotation(mouse_annotation)


    #CLOSE THE INPUT FILES
    mouse_gaf.close()
    rat_gaf.close()

    print("Closed input files.")

    #FIX THE TEST FILE:
    #doesnt work yet because there are no actual go-terms in the test data...
    perf_scores = []
    go_tree = read_go_tree("go-basic.obo")
    for prot_key in rat_dict.keys():
        rat_dict[prot_key] = fix_go(rat_dict[prot_key], go_tree)
        #true_vec, pred_vec = Vectorize true set and pred set.
        #perf_score = Evaluate true vec, pred_vec
        #append perf score to perf_scores.


    print("Fixed tree of true annotation.")


    #Vectorizer: Als een true eiwit of term niet wordt gevonden in de test set, voeg hier alleen zeros toe.
    #Dictionary van pred bij eiwit zonder terms: eiwit_id : []


    # Call class
    converter = Converter()
    #FIX THE PREDICTOR OUTPUT:
    for prot_key, terms in mouse_dict.items():
        mouse_dict[prot_key] = fix_go(mouse_dict[prot_key], go_tree)
        converter.get_terms_unique({prot_key : terms})
        converter.get_training_terms({prot_key: terms})

    print("Fixed tree of predicted annotation")

    #VECTORIZE THE TEST AND PREDICTION FILES
    # Step 1: All test/training unique terms. Training terms will be called in the fixx_go loop:
    converter.get_terms_unique(rat_dict)
    converter.get_test_terms(rat_dict)
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
    #Plot list of miss data fracs vs list of perf. scores.

main()
