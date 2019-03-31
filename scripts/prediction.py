#!/usr/bin/env python3
from classes.fix_go import fix_go
from classes.fix_go import read_go_tree
from classes.true_ann_parser import parse_true_annotation
from classes.Evaluator import Evaluator
from classes.plotter import Plotter
from classes.class_splitter import Splitter
from classes.klasse_avaluator import Converter


def main():
    # Step 1: Import script input files
    mouse_gaf, rat_gaf, blast_uniprot = import_files("files/goa_mouse.gaf", "files/goa_rat.gaf", 'files/out.txt')
    
    # Step 2: convert input files to analysable files
    blast_input, blast_output = blast(blast_uniprot)
    print("data has been imported")

    # Step 2: determine the biological proces:
    processen = ["biological_process", "molecular_function", "cellular_component"]
    for proces in processen:
        go_tree, uniek = read_go_tree("files/go-basic.obo", proces)
        true_ids, dict_mouse = true_con(mouse_gaf, blast_input, go_tree)

        # Step 3: Create a numpy array and call the plotter
        plotter = Plotter()
        converter = Converter(uniek)
        true_vector = converter.fill_np(len(true_ids), dict_mouse, true_ids)

        # Step 4: determine fractions and loop to cut the file for prediction.
        fractions = [100, 90, 80, 70, 60, 50]
        for fraction in fractions:
            rat_dict = get_test_data(fraction, rat_gaf, blast_output, go_tree, blast_input)

            # Step 5: Create a numpy array for the prediction and get the vectors.
            pred_vector = converter.set_training_np(rat_dict, true_ids)

            # Step 6: Get evaluation score:
            evaluator = Evaluator(true_vector, pred_vector)
            f1_scores = evaluator.get_f1()
            gem = f1_scores.mean()

            # Step 7: Plot
            plotter.get_score(fraction, gem)
        plotter.plot_performance(proces)
    plotter.get_plot()


# Get all known annotation from the rattus from the blast output file.
# The blast input id is put for the blast output search.
def get_test_data(fraction, rat_gaf, blast_output, tree, blast_input):
    sample = Splitter(fraction, rat_gaf).splitter()
    true_set = parse_true_annotation(sample)
    rat_dict = {}
    for index, ids in enumerate(blast_output):
        if ids in true_set:
            rat_dict[blast_input[index]] = fix_go(true_set[ids], tree)
    return rat_dict


# Get the true annotation from the mouse for all proteins in the blast input file.
def true_con(mouse, blast, tree):
    true_set = parse_true_annotation(mouse)
    dict = {}
    true_ids = {}
    getal = 0
    for ids in blast:
        if ids in true_set:
            termen = fix_go(true_set[ids], tree)
            dict[ids] = termen
            if len(termen) > 0:
                true_ids[ids] = getal
                getal += 1
    return true_ids, dict

# Get the input and output of the BLAST output file.
def blast(blast):
    input, output = [], []
    for regels in blast:
        regel = regels.split("|")
        if len(input) == 0:
            input.append(regel[1])
            output.append(regel[-2])
        else:
            if regel[1] not in input[-1]:
                input.append(regel[1])
                output.append(regel[-2])
    return input, output


# Import mouse annotation, rat annotation, and the blast output file.
def import_files(mouse, rat, blast):
    mouse_gaf = open(mouse, "r")
    rat_gaf = open(rat, "r")
    blast_uniprot = open(blast, 'r')
    mouse_annotation = mouse_gaf.readlines()
    rat_annotation = rat_gaf.readlines()
    blast_in_out = blast_uniprot.readlines()
    mouse_gaf.close()
    rat_gaf.close()
    blast_uniprot.close()
    return mouse_annotation, rat_annotation, blast_in_out


main()