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
from goarraymaker import GoArrayMaker




        
        

def main():
    #READ THE INPUT FILES
    global go_tree
    mouse_gaf = open("goa_mouse.gaf", "r")
    rat_gaf = open("goa_rat.gaf", "r")
    ref_uniprot = open('Refseqtouniprotkb.txt', 'r')
    mouse_annotation = mouse_gaf.readlines()
    rat_annotation = rat_gaf.readlines()
    uniprot_file = ref_uniprot.readlines()
    print("Loaded input files.")

    #CLOSE THE INPUT FILES
    mouse_gaf.close()
    rat_gaf.close()
    ref_uniprot.close()

    #Determine which columns has the uniprot data:
    uniprot_column_index = 0
    for index, column in enumerate(uniprot_file[0].strip().split(" ")):
        if "." and "_" not in column:
            uniprot_column_index = index
            break

    #Add all the uniprotKB codes to the uniprot_code_list
    uniprot_codes = []
    for line in uniprot_file:
        uniprot_codes.append(line.strip().split(" ")[uniprot_column_index])

    print("Loaded in all the UniprotKB codes.")

    #example: check missing data on 5 points (100%, 80%, 60%, 40%, 20%)
    fractions = [20, 40, 60, 80, 100]

    #Make a list for the performance values
    perf_array = []

    # GET PARSED TRUE (RAT) ANNOTATION:
    true_dict = parse_true_annotation(rat_annotation)

    
    print("Parsed input data.")

    go_tree = read_go_tree("go-basic.obo")
    print("Read GO-tree.")

    #Initialize GoArrayMaker
    arraymaker = GoArrayMaker(go_tree, uniprot_codes + list(true_dict.keys()))

    true_set = arraymaker.make_go_array(true_dict)

    print("True annotation vectorized.")
    #Calling the predictor class with the blast method ang give the uniprot list as an argument.
    blast_predictor = Predictor("blast", uniprot_codes)

    #Loop through each fraction, doing the prediction, go-tree-fixing, vectorization and evaluation for each.
    for frac in fractions:
        #Get a sample of the rat-gaf with missing data.
        sample = Splitter(frac, rat_annotation).splitter()
        print("gaf-sample of " + str(frac) + "% taken.")
        #Predict the GO-terms for the mouse by linking the rat-hits to the rat-gaf.
        prediction_set = blast_predictor.blast(sample)
        print("Predicted annotation for the sample.")
        #Fix the GO-terms according to the GO-tree.
        for protein_key in prediction_set:
            prediction_set[protein_key] = fix_go(prediction_set[protein_key], go_tree)

        #Vectorize the true and predicted annotations, give the go-tree for the columns.
        #Turn dataset into numpy array
        t0 = time.time()
        pred_set = arraymaker.make_go_array(prediction_set)
        print("took:", time.time() -t0, "for:", len(prediction_set))
        print(pred_set)
        
        
        print("Adjusted GO-terms according to GO-tree.")

        #Evaluate the run:
        evaluator = Evaluator(true_set, pred_set)
        f1_scores = evaluator.get_f1()
        print("Average f1:", f1_scores.mean())
        perf_array.append(f1_scores.mean())
        print("Evaluated prediction method.")

    #Plot the evaluation
    #plot = Plotter.plot_performance(fractions, perf_array)

    """
    NOTES:
    Vectorizer: Als een true eiwit of term niet wordt gevonden in de test set, voeg hier alleen zeros toe.
    Dictionary van pred bij eiwit zonder terms: eiwit_id : []
    """

main()
