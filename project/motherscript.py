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
    rat_annotation = rat_annotation[:10000]
    true_set = parse_true_annotation(rat_annotation)
    print("Parsed true-annotation.")

    # Step 4: Import data from obo file
    go_tree = read_go_tree("files/go-basic.obo")
    print("GO-tree annotation read.")

    #Add the GO-parents to the true annotation.
    for protein_key in true_set:
        true_set[protein_key] = fix_go(true_set[protein_key], go_tree)

    print("Added GO-parents to the true annotation.")
    converter = Converter()
    converter.set_terms_unique_test(true_set)
    converter.set_np()
    converter.set_test_np()
    print("Made arrays for use in the Evaluator.")

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
    fractions = [100, 90, 80, 70, 60, 50, 40, 30, 20, 10]
    plotter = Plotter()


    # Loop through all fractions till the plotter input.
    for fraction in fractions:
        print("\nPREDICTION RUN FOR %s%% OF THE PREDICTED ANNOTATION:\n" % str(fraction))
        sample = Splitter(fraction, prediction_set).splitter()
        print("Sampled %s%% from the predicted annotation." % str(fraction))

        # Step 6: Run the Fix go, and create a training numpy array:
        # Set training array in Evaluator to []
        temp = {}
        for protein_key in sample:
            temp[protein_key] = fix_go(sample[protein_key], go_tree)
            converter.set_training_np(temp)
            temp = {}
        print("Added GO-parent tree for the predicted annotation.")

        # Step 7: Call true/false training set
        true_vector, pred_vector = converter.get_array()
        print("Filled arrays with the predicted annotation.")

        # Step 8: Evaluate
        evaluator = Evaluator(true_vector, pred_vector)
        f1_scores = evaluator.get_f1()
        gem = f1_scores.mean()
        print("Average f1:", gem)
        print("Evaluated prediction with %s%% of the prediction data." % str(fraction))


        # Step 9: plot
        plotter.add_score(fraction, gem)
        print("Saved evaluation in plotter class.")

        # Call the converter class again
        converter = Converter()
        converter.set_terms_unique_test(true_set)
        converter.set_np()
        converter.set_test_np()


    print(plotter.plot_performance())








































main()
