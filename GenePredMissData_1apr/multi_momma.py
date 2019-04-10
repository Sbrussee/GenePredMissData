#!/usr/bin/env python3
import time
import os
import importlib
from multiprocessing import Process, Queue
from classes.arguments import *
from classes.fix_go import Go_Fixer
from classes.gaf_parser import gaf_parse
from classes.Evaluator import Evaluator
from classes.plotter import Plotter
from classes.backup.Dict2Array import Dict2Array
from classes.filter_gaf import filter_gaf
from classes.splitter import split
from classes.Predictor import Predictor

def step(requests, results, predictor, testdata, traindata, testclass_array,
         trainclass, arraymaker, gofixer, gofix):
    while requests.qsize() > 0:
        fraction = requests.get()
        sample = split(trainclass, fraction)
        predictor.set_trainclass(gaf_parse(sample))
        predictions = predictor.get_predictions(testdata)
        if gofix:
            pred_array = arraymaker.make_array(predictions, gofixer.fix_go)
        else:
            pred_array = arraymaker.make_array(predictions,
                                               gofixer.replace_obsolete_terms)
        evaluator = Evaluator(testclass_array, pred_array)
        f1_scores = evaluator.get_f1()
        stdev = f1_scores.std()
        average = f1_scores.mean()
        results.put((fraction, average, stdev))


def main():
    args = get_args()
    gofix = not "nogofix" in args
    threads = args["threads"]
    if threads == "*":
        threads = os.sysconf("SC_NPROCESSORS_ONLN")
    print("Using %s threads"%threads)
    print("Loading input files")
    testclass_file = open(args["testgaf"], "r")
    trainclass_file = open(args["traingaf"], "r")
    traindata_file = open(args["traindata"], "r")
    testdata_file = open(args["testdata"], "r")
    testclass = testclass_file.readlines()
    trainclass = trainclass_file.readlines()
    traindata = traindata_file.readlines()
    testdata = testdata_file.readlines()
    testclass_file.close()
    trainclass_file.close()
    traindata_file.close()
    testdata_file.close()
    
    print("Parsing annotation")
    testclass = gaf_parse(filter_gaf(testclass, args["evidence"]))
    trainclass = filter_gaf(trainclass)
    
    print("Reading GO-tree")
    gofixer = Go_Fixer("files/go-basic.obo")
    
    print("Indexing all GO-terms")
    allterms = []
    for terms in list(gaf_parse(trainclass).values()) + \
        list(testclass.values()):
        if gofix:
            terms = gofixer.fix_go(terms)
        allterms.extend(terms)
    extend = 1
    arraymaker = Dict2Array(allterms, testclass, extend)
    plotter = Plotter()
    predictor = Predictor(traindata, extend)
    
    if gofix:
        testclass_array = arraymaker.make_array(testclass, gofixer.fix_go)
    else:
        testclass_array = arraymaker.make_array(testclass,
                                                gofixer.replace_obsolete_terms)

    print("\nSTARTING")
    requests = Queue()
    for fraction in range(100, 0, -args["stepsize"]):
        for r in range(0, args["repeats"]):
            requests.put(fraction)

    total = requests.qsize()
    processes = []
    results = Queue()
    done = 0
    print("Progress: 0%")
    for x in range(threads):
        p = Process(target = step, args = (requests, results, predictor,
                                           testdata, traindata,
                                           testclass_array, trainclass,
                                           arraymaker, gofixer, gofix))
        p.start()
        processes.append(p)
    file = open("results.tsv","w")
    file.write("fraction\tresult\n")
    while total - done > 0:
        r = results.get()
        done += 1
        print("Progress:", str(round(100 - (total - done) / total * 100)) +
              "%")
        file.write(str(r[0]) + "\t" + str(r[1]) + "\n")
        plotter.add_score(r[0], r[1], r[2])
        time.sleep(1)
    file.close()
    plotter.plot_performance()

main()
