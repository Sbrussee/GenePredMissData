#!/usr/bin/env python3
import time
from classes.arguments import *
from classes.fix_go import Go_Fixer
from classes.gaf_parser import gaf_parse
from classes.Evaluator import Evaluator
from classes.plotter import Plotter
from classes.backup.Dict2Array import Dict2Array
from classes.filter_gaf import filter_gaf
from classes.splitter import split
from classes.Predictor import Predictor

def main():
    #GET commandline arguments
    args = get_args()
    
    #OPEN files
    testclass_file = open(args["testgaf"], "r")
    trainclass_file = open(args["traingaf"], "r")
    traindata_file = open(args["traindata"], "r")
    testdata_file = open(args["testdata"], "r")

    #READ lines
    print("Loading input files")
    testclass = testclass_file.readlines()
    trainclass = trainclass_file.readlines()
    traindata = traindata_file.readlines()
    testdata = testdata_file.readlines()
    testclass_file.close()
    trainclass_file.close()
    traindata_file.close()
    testdata_file.close()

    #PARSE annotation
    print("Parsing annotation")
    testclass = gaf_parse(filter_gaf(testclass, args["evidence"], args["domain"]))
    trainclass = filter_gaf(trainclass, args['evidence'], args['domain'])

    #INIT gofixer
    print("Reading GO-tree")
    gofixer = Go_Fixer("files/go-basic.obo")

    #INIT arraymaker
    print("Indexing all GO-terms")
    allterms = []
    for terms in list(gaf_parse(trainclass).values()) + \
        list(testclass.values()):
        allterms.extend(gofixer.fix_go(terms))
    extend = 1
    arraymaker = Dict2Array(allterms, testclass, extend)

    #INIT plotter
    plotter = Plotter(args['evaluator'])

    #INIT predictor
    predictor = Predictor(traindata, extend)

    #MAKE true vector
    print("Making correct vector")
    testclass_array = arraymaker.make_array(testclass, gofixer.fix_go)
    
    #START mainloop
    for fraction in range(100, 0, -args["stepsize"]):
        for round in range(0, args["repeats"], 1):
            #MEASURE start time
            t0 = time.time()

            #PRINT round info
            print("\nPREDICTION RUN %s FOR %s%% OF THE PREDICTED ANNOTATION:" % (str(round + 1), str(fraction)))

            #SPLIT prediction set
            sample = split(trainclass, fraction)

            #SET prediction sample
            predictor.set_trainclass(gaf_parse(sample))

            #GET prediction
            predictions = predictor.get_predictions(testdata)

            #MAKE prediction array
            print("Converting prediction to array")
            pred_array = arraymaker.make_array(predictions, gofixer.fix_go)

            #CALCULATE evaluation
            print("Evaluating results")
            t1 = time.time()
            evaluator = Evaluator(testclass_array, pred_array, args['evaluator'])
            evaluations = evaluator.get_evaluation()
            for metric, average in evaluations.items():
                print(metric, average)

            #DISPLAY evaluation
            print("Evaluated prediction with %s%% of the prediction data." %
                  str(fraction))
            print("Evaluation took: ", '{0:.3g}'.format(time.time() - t1), "seconds")

            #ADD evaluation to plotter
            plotter.add_score(fraction, evaluations)

            #DISPLAY round time
            print("TOOK:", '{0:.3g}'.format(time.time() - t0), "seconds")

    #PLOT performance
    plotter.plot_performance()

main()
