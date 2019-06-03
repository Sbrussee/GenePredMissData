#!/usr/bin/env python3
import time
import os
import importlib
import re
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
        
    

def step(requests, results, predictor, testdata, traindata, testclass_array,
         trainclass, arraymaker, gofixer, gofix, evaluators, t, plst):


    while requests.qsize() > 0:
        fraction = requests.get()
        sample = split(trainclass, fraction)

        """Besthits: How many predictors do you want?"""
        besthits = 1

        """train_matrix: Define the gaf file in a matrix"""
        train = train_matrix()
        matrix, go_index_reverse, rat_index = train.convert(gaf_parse(sample))

        """If you want only annotated hits"""
        only_annotated = True
        predictor.correct_traindata(besthits, rat_index, only_annotated)

        """Get the train data"""
        traindata = predictor.get_train()

        """If plst method has to be performed:"""
        if plst > 0:
            a = call_PLST()
            matrix = a.train(matrix, plst, PLST_class)

        """Make the predictions:"""
        matrix, rat_index = predictor.get_predictions(testdata, matrix, rat_index)

        """If the plst method has been performed, then convert the matrix to the original score"""
        if plst > 0:
            matrix = a.inverse(matrix)
            del a

        """Put the matrix results in a dictionaire"""
        predictions = train.back_convert(matrix, rat_index, go_index_reverse, traindata)

        """Delete some variables out of memory"""
        del matrix, traindata, rat_index, go_index_reverse, train

        """Create a lil matrix from the dictionaire"""
        if gofix:
            pred_array = arraymaker.make_array(predictions, gofixer.fix_go, predictor.get_dtype())
        else:
            pred_array = arraymaker.make_array(predictions,
                                               gofixer.replace_obsolete_terms, predictor.get_dtype())

        evaluator = Evaluator(testclass_array, pred_array, evaluators)
        evaluation = evaluator.get_evaluation()
        results.put((fraction, evaluation))


def main():
    #args = get_args()
    #print(args)
    arglist = [
        {'stepsize': 50, 'traindata': 'files/blast_besthit_traindata_mouserat', 'traingaf': './files/goa_rat.gaf', 'testdata': './files/blast_besthit_testdata_mouse', 'testgaf': './files/goa_mouse.gaf', 'predictor': 'predictors/blast.py', 'evaluator': ['average_precision'], 'predargs': 'blast', 'plotter': 'line', 'evidence': ('EXP', 'IDA', 'IPI', 'IMP', 'IGI', 'IEP', 'HTP', 'HTP', 'HDA', 'HMP', 'HGI', 'HEP', 'IBA', 'IBD', 'IKR', 'IRD', 'ISS', 'ISO', 'ISA', 'ISM', 'IGC', 'RCA', 'TAS', 'NAS', 'IC', 'ND', 'IEA', 'IEA'), 'domain': ('C', 'F', 'P'), 'repeats': 1, 'threads': 2, 'nogofix': '', 'plst': -1},
        {'stepsize': 50, 'traindata': 'files/blast_onlyannotated_traindata_rat', 'traingaf': './files/goa_rat.gaf', 'testdata': './files/blast_onlyannotated_testdata_mouse', 'testgaf': './files/goa_mouse.gaf', 'predictor': 'predictors/blast.py', 'evaluator': ['average_precision'], 'predargs': 'blast', 'plotter': 'line', 'evidence': ('EXP', 'IDA', 'IPI', 'IMP', 'IGI', 'IEP', 'HTP', 'HTP', 'HDA', 'HMP', 'HGI', 'HEP', 'IBA', 'IBD', 'IKR', 'IRD', 'ISS', 'ISO', 'ISA', 'ISM', 'IGC', 'RCA', 'TAS', 'NAS', 'IC', 'ND', 'IEA', 'IEA'), 'domain': ('C', 'F', 'P'), 'repeats': 1, 'threads': 2, 'nogofix': '', 'plst': -1}
               ]
    plotter = Plotter()
    methodlist = []
    number = 0
    for args in arglist:
        argname = re.split('/|\.', args["predictor"])[-2]
        if argname not in methodlist:
            number += 1
            methodlist.append(argname)
        else:
            methodlist.append(argname+'n'+str(number))


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
        testclass = testclass_file.readlines()[:10000]
        trainclass = trainclass_file.readlines()[:10000]
        traindata = traindata_file.readlines()[:10000]
        testdata = testdata_file.readlines()[:10000]
        testclass_file.close()
        trainclass_file.close()
        traindata_file.close()
        testdata_file.close()
        
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
                terms = gofixer.fix_go(terms)
            allterms.extend(terms)
        if "predargs" in args:
            predictor = Predictor(traindata, args["predargs"])
        else:
            predictor = Predictor(traindata, None)
        arraymaker = Dict2Array(allterms, testclass)
        
        if gofix:
            testclass_array = arraymaker.make_array(testclass, gofixer.fix_go, bool)
        else:
            testclass_array = arraymaker.make_array(testclass,
                                                gofixer.replace_obsolete_terms, bool)

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
        file = open("results.tsv","w")
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
                file.write(str(r[0]) + "\t" + str(metric) + "\t" + str(evaluation)
                           + "\n")
            plotter.add_score(r[0], r[1])
        file.close()


    plotter.plot_performance(args["plst"], methodlist)

main()
