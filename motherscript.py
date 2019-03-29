#!/usr/bin/env python3
from classes.fix_go import fix_go
from classes.fix_go import read_go_tree
from classes.true_ann_parser import parse_true_annotation
from classes.Evaluator import Evaluator
from classes.plotter import Plotter
from classes.class_splitter import Splitter
from classes.predictorfile import Predictor
from classes.klasse_avaluator import Converter


def main():
    #READ THE INPUT FILES
    global go_tree
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
    rat_annotation = rat_annotation[:1000]
    true_set = parse_true_annotation(rat_annotation)
    converter = Converter()
    converter.set_terms_unique_test(true_set)
    converter.set_np()
    converter.set_test_np()

    # Step 2: Create the prediction uniprot ids
    uniprot_column_index = 0
    for index, column in enumerate(uniprot_file[0].strip().split(" ")):
        if "." and "_" not in column:
            uniprot_column_index = index

    uniprot_codes = []
    for line in uniprot_file:
        uniprot_codes.append(line.strip().split(" ")[uniprot_column_index])
    print("loaded in all UniprotKB codes")


    # Step 3: Put the uniprot ids in the blast memory and check the blast prediction.
    blast_predictor = Predictor("blast", uniprot_codes)
    prediction_set = blast_predictor.blast(rat_annotation)
    print("blast_predictor set")

    # Step 4: Import data from obo file
    go_tree = read_go_tree("files/go-basic.obo")
    print("go_tree set")


    # Stap 5: Detemine fraction data and call plotter
    fractions = [100, 80, 60, 40]
    plotter = Plotter()


    # Loop through all fractions till the plotter input.
    for fraction in fractions:
        sample = Splitter(fraction, prediction_set).splitter()
        print("sample set")

        # Step 6: Run the Fix go, and create a training numpy array:
        # Set treaining array in avaluator to []
        temp = {}
        for protein_key in sample:
            temp[protein_key] = fix_go(sample[protein_key], go_tree)
            converter.set_training_np(temp)
            temp = {}

        # Step 7: Call true/false training set
        true_vector, pred_vector = converter.get_array()

        # Step 8: Evaluate
        evaluator = Evaluator(true_vector, pred_vector)
        f1_scores = evaluator.get_f1()
        gem = f1_scores.mean()
        print("Average f1:", gem)


        # Step 9: plot
        plotter.get_score(fraction, gem)

        # Call the converter class again
        converter = Converter()
        converter.set_terms_unique_test(true_set)
        converter.set_np()
        converter.set_test_np()


    print(plotter.plot_performance())








































main()
