#!/usr/bin/env python3
import time
import os
import importlib
import re
import datetime
from multiprocessing import Process, Queue
from classes.arguments import *
from classes.fix_go import Go_Fixer
from classes.gaf_parser import gaf_parse
from classes.Evaluator import Evaluator
from classes.plotter import Plotter
from classes.Dict2Array import Dict2Array
from classes.filter_gaf import filter_gaf
from classes.splitter import split
from classes.lsdr import PLST as PLST_class
from classes.call_PLST import call_PLST
from classes.train_matrix import train_matrix

class thread_print:
    def __init__(self):
        self.q = Queue()
    
    def print(self, toprint):
        self.q.put(toprint)

    def display(self):
        if self.q.qsize() > 0:
            print(self.q.get())

class tprint:
    def print(self, toprint):
        print(toprint)
    

def step(requests, results, predictor, testdata, traindata, testclass_array,
         trainclass, arraymaker, gofixer, gofix, evaluators, t, plst):
    while requests.qsize() > 0:
        #t.print("START")
        fraction = requests.get()
        sample = split(trainclass, fraction)
        train = train_matrix()
        matrix, go_index_reverse, rat_index = train.convert(gaf_parse(sample))
        #t.print("AFTER TRAIN CONVERT")
        if plst > 0:
            #t.print("STARTING a.train")
            a = call_PLST()
            matrix = a.train(matrix, plst, PLST_class)
            #t.print("RAN a.train")
        #t.print("STARTING PREDICTION")
        matrix, rat_index = predictor.get_predictions(testdata, matrix, rat_index)
        if plst > 0:
            #t.print("STARTING a.inverse")
            matrix = a.inverse(matrix)
            del a
            #t.print("RAN a.inverse")
        #t.print("STARTING backconvert")
        predictions = train.back_convert(matrix, rat_index, go_index_reverse, predictor.get_train())
        del matrix, rat_index, go_index_reverse, train
        #t.print("STARTING GOFIX")
        if gofix:
            pred_array = arraymaker.make_array(predictions, gofixer.fix_go, predictor.get_dtype(), t)
        else:
            pred_array = arraymaker.make_array(predictions,
                                               gofixer.replace_obsolete_terms, predictor.get_dtype(), t)
        #t.print("STARTING EVAL")
        evaluator = Evaluator(testclass_array, pred_array, evaluators)
        
        evaluation = evaluator.get_evaluation()
        results.put((fraction, evaluation))


def main():
    title, multargs = get_args()
    plotter = Plotter()
    methodlist = []
    plotconfig = []
    number = 0
    file = open("results.tsv","w")
    file.write("title: " + title + "\n")
    for legend in multargs:
        if len(multargs) > 1:
            print("\nRUN:", legend)
            
        methodlist.append(legend)
        args = multargs[legend]
        plotconfig.append((args["color"], args["linetype"]))
        #print(plotconfig)
        argname = re.split('/|\.', args["predictor"])[-2]
        modname = args["predictor"].split(".")[0].replace("/", ".")
        print("Using predictor:", modname)
        Predictor = importlib.import_module(modname).Predictor
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

        t = tprint()
        
        print("Parsing annotation")
        testclass = gaf_parse(filter_gaf(testclass, args["evidence"],
                                         args["domain"]))
        trainclass = filter_gaf(trainclass, args["evidence"], args["domain"])
        
        print("Reading GO-tree")
        gofixer = Go_Fixer("files/go-basic.obo")
        
        print("Indexing all GO-terms")
        allterms = []
        for terms in list(gaf_parse(trainclass).values()) + \
            list(testclass.values()):
            if gofix:
                terms = gofixer.fix_go(terms, t)
            allterms.extend(terms)
        if "predargs" in args:
            predictor = Predictor(traindata, args["predargs"])
        else:
            predictor = Predictor(traindata, None)
        arraymaker = Dict2Array(allterms, testclass)
        
        if gofix:
            testclass_array = arraymaker.make_array(testclass, gofixer.fix_go, bool, t)
        else:
            testclass_array = arraymaker.make_array(testclass,
                                                gofixer.replace_obsolete_terms, bool, t)

        print("\nSTARTING")
        requests = Queue()
        for fraction in range(100, 0, -args["stepsize"]):
            for r in range(0, args["repeats"]):
                requests.put(fraction)

        total = requests.qsize()
        processes = []
        results = Queue()
        t = thread_print()
        done = 0
        
        print("Progress: 0%")
        for x in range(threads):
            p = Process(target = step, args = (requests, results, predictor,
                                               testdata, traindata,
                                               testclass_array, trainclass,
                                               arraymaker, gofixer, gofix,
                                               args["evaluator"], t, args["plst"]))
            p.start()
            processes.append(p)
        file.write("legend: " + legend + "\nlinetype: " +
                   args["linetype"] + "\ncolor: " + args["color"] + "\n" )
        file.write("fraction\tmetric\tresult\n")
        reslist = []
        while total - done > 0:
            t.display()
            if results.qsize() > 0:
                r = results.get()
                done += 1
                print("Progress:", str(round(100 - (total - done)
                                             / total * 100)) + "%")
                reslist.append(r)
            time.sleep(0.1)
        for r in sorted(reslist, key=lambda x: x[0]):
            for metric, evaluation in r[1].items():
                print("Fraction:", r[0], "Metric:", metric, "Evaluation:",
                      evaluation)
                file.write(str(r[0]) + "\t" + str(metric) + "\t" + str(evaluation) + ";\t")
            plotter.add_score(r[0], r[1])
            file.write("\n")
    file.close()
    extrastring = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    plotter.plot_performance(title, methodlist, plotconfig, extrastring)
    os.rename("results.tsv", title + extrastring)

main()
