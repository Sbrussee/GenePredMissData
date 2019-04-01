#!/usr/bin/env python3
import time
from classes.fix_go import Go_Fixer
from classes.true_ann_parser import parse_true_annotation
from classes.Evaluator import Evaluator
from classes.plotter import Plotter
from classes.class_splitter import Splitter
from classes.predictorfile import Predictor
from classes.klasse_avaluator import Converter
from classes.Dict2Array import Dict2Array


def main():
    #READ THE INPUT FILES
    mouse_gaf = open("files/goa_mouse.gaf", "r")
    rat_gaf = open("files/goa_rat.gaf", "r")
    ref_uniprot = open('files/Refseqtouniprotkb.txt', 'r')
    mouse_annotation = mouse_gaf.readlines()
    rat_annotation = rat_gaf.readlines()
    uniprot_file = ref_uniprot.readlines()
    
    print("Loaded input files.")

    #CLOSE THE INPUT FILES
    mouse_gaf.close()
    rat_gaf.close()
    ref_uniprot.close()


    # Stap 1: Get the true data and create a nupy
    #rat_annotation = rat_annotation[:100]
    true_set = parse_true_annotation(rat_annotation)
    print("Parsed true-annotation.")

    # Step 4: Import data from obo file
    gofixer = Go_Fixer("files/go-basic.obo")
    print("GO-tree annotation read.")

    # Step 2: Create the prediction uniprot ids
    uniprot_column_index = 0
    for index, column in enumerate(uniprot_file[0].strip().split(" ")):
        if "." and "_" not in column:
            uniprot_column_index = index

    uniprot_codes = []
    for line in uniprot_file:
        uniprot_codes.append(line.strip().split(" ")[uniprot_column_index])
    print("Loaded in all UniprotKB codes.")

    # Step 3: Put the uniprot ids in the blast memory and check the blast prediction.
    blast_predictor = Predictor("blast", uniprot_codes)
    prediction_set = blast_predictor.blast(rat_annotation)
    print("BLAST-prediction obtained.")

    
    # Stap 5: Detemine fraction data and call plotter
    #fractions = [100, 90, 80, 70, 60, 50, 40, 30, 20, 10]
    fractions = range(100, 0, -10)
    plotter = Plotter()

    # INIT ArrayMaker
    arraymaker = Dict2Array(gofixer.get_go_tree().keys(), list(prediction_set.keys())
                            + list(true_set.keys()))
    # Making True vector and adding parent GO-Therms
    print("Making True vector")
    true_vector = arraymaker.make_array(true_set, gofixer.fix_go)

    # Loop through all fractions till the plotter input.
    for fraction in fractions:
        t0 = time.time()
        print("\nPREDICTION RUN FOR %s%% OF THE PREDICTED ANNOTATION:\n" % str(fraction))
        sample = Splitter(fraction, prediction_set).splitter()
        print("Sampled %s%% from the predicted annotation." % str(fraction))
        
        # Step 7: Call true/false training set
        #true_vector, pred_vector = converter.get_array()
        print("Making prediction vector")
        pred_vector = arraymaker.make_array(sample, gofixer.fix_go)
        print("Filled arrays with the predicted annotation.")

        # Step 8: Evaluate
        t1 = time.time()
        evaluator = Evaluator(true_vector, pred_vector)
        f1_scores = evaluator.get_f1()
        gem = f1_scores.mean()
        print("Average f1:", gem)
        print("Evaluated prediction with %s%% of the prediction data." % str(
            fraction))
        print("Evaluation took: ", time.time() - t1)
        # Step 9: plot
        plotter.add_score(fraction, gem)
        print("Saved evaluation in plotter class.")
        print("TOOK:", time.time() - t0)



    plotter.plot_performance()



main()
