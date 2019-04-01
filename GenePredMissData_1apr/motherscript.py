#!/usr/bin/env python3
import time
from classes.fix_go import Go_Fixer
from classes.gaf_parser import gaf_parse
from classes.Evaluator import Evaluator
from classes.plotter import Plotter
from classes.class_splitter import Splitter
from classes.Dict2Array import Dict2Array


def main():
    #OPEN files
    mouse_gaf = open("files/goa_mouse.gaf", "r")
    rat_gaf = open("files/goa_rat.gaf", "r")
    trainfile = open("files/mouseratblast", "r")

    #READ lines
    print("Loading input files")
    mouse_annotation = mouse_gaf.readlines()
    rat_annotation = rat_gaf.readlines()
    traindata = trainfile.readlines()
    mouse_gaf.close()
    rat_gaf.close()
    trainfile.close()

    #PARSE true annotation
    print("Parsing true annotation")
    true_set = gaf_parse(mouse_annotation)

    #INIT gofixer
    print("Reading GO-tree")
    gofixer = Go_Fixer("files/go-basic.obo")

    #INIT arraymaker
    arraymaker = Dict2Array(gofixer.get_go_tree().keys(), true_set.keys())

    #INIT plotter
    plotter = Plotter()

    #MAKE true vector
    print("Making True vector")
    true_vector = arraymaker.make_array(true_set, gofixer.fix_go)
    

    for fraction in range(100, 0, -10):
        
        #MEASURING start time
        t0 = time.time()

        print("\nPREDICTION RUN FOR %s%% OF THE PREDICTED ANNOTATION:\n" % str(fraction))
        
        #SPLITTING prediction set
        sample = Splitter(fraction, prediction_set).splitter


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
