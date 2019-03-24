#!/usr/bin/env python3
import importlib
import random
from arguments import get_args
import time

import numpy as np
import matplotlib as mpl

from fix_go import fix_go
from fix_go import read_go_tree
from Evaluator import Evaluator
from Plotter import Plotter
from klasse_avaluator import Converter
from klasse_splitter import Splitter

def index_gaf(filename, evidence):
    dex = []
    with open(filename) as file:
        pos = file.tell()
        line = file.readline()
        while line:
            if evidence != "*":
                if line[0] != "#" and line[0] != "!":
                    line = line.split("\t")
                    if line[6] in evidence:
                        dex.append(pos)
            else:
                dex.append(pos)
            pos = file.tell()
            line = file.readline()
    file.close()
    return dex

def slice_gaf(infile, outfile, dex, percent):
    size = len(dex)
    with open(infile, "r") as infile:
        with open(outfile, "w") as outfile:
            for i in range(int((percent / 100) * len(dex))):
                choice = random.randint(0, size - 1)
                infile.seek(dex[choice])
                del dex[choice]
                size -= 1
                outfile.write(infile.readline())
    outfile.close()
    infile.close()

    

def main():
    #GET THE ARGUMENTS:

    #argstore = get_args()

    #example: check missing data on 5 points (100%, 80%, 60%, 40%, 20%)
    fractions = [0, 20, 40, 60, 80, 100]

    #splice the data in 5 files with different fractions missing:
    #Using the indexing method:
    dex = index_gaf("mouse.gaf", ["ND", "ISO", "IMP", "IDA", "EXP"])
    for frac in fractions:
        print(frac)
        slice_gaf("mouse.gaf", "mouse_" + str(frac) + ".gaf", dex, frac)
        print("done")

    #Using the original splicing method:
    #Get line count for mouse file:
    file_length = sum(1 for line in open('mouse.gaf'))
    for frac in fractions:
        print(frac)
        split = Splitter(frac, file_length, 'mouse.gaf', "mouse_" + str(frac) + ".gaf")
        split.splitter()
        print("done")
    #SAMPLE CODE PREDICTOR:
    #example: We want to predict 10 times for each fraction
    num_of_pred_per_frac = 10
    #for frac in fractions:
    #    for times in range(0, num_of_pred_per_frac):
    #        pred = Predictor(method)
    #        results = Predictor.predict()


    #BECAUSE THERE IS NO PREDICTOR YET:
    # The set with for each term the right assignment.
    true_assignment = {
        "gen1": ["go1", "go22", "go13", "go10", "go5", "go6", "go7", "go8", "go9", "go10", "go11", "go12", "go13"],
        "gen3": ["go14", "go15", "go136", "go17", "go22", "go33", "go11", "go8", "go9", "go112", "go119", "go159", "go13"],
        "gen4": ["go1", "go2", "go35", "go4", "go45", "go56", "go755", "go11", "go99", "go10", "go11", "go12", "go133"],
        "gen5": ["go1", "go12", "go3", "go44", "go454", "go20", "go17", "go98", "go93", "go10", "go11", "go12", "go13"],
        "gen2": ["go1", "go2", "g4o3", "go4", "go5", "go6", "go7", "go8", "go9", "go10", "go11", "go12", "go1344"]}

    # The set which will be made from the predictor and fix_go classe.
    training_assignment = {
        "gen3": ["go11", "go2", "go1", "go10", "go51", "go62", "go37", "go8", "go94", "go10", "go11", "go12", "go13"],
        "gen4": ["go14", "go15", "go136", "go1", "go222", "go332", "go131", "go84", "go91", "go112", "go11", "go15", "go13"],
        "gen1": ["go1", "go2", "go35", "go4", "go45", "go56", "go11", "go99", "go10", "go11", "go12", "go133"],
        "gen5": ["go1", "go12", "go3", "go44", "go454", "go20", "go17", "go12", "go13"],
        "gen2": ["go1", "go23", "go43", "go25", "go16", "go17", "go8", "go9", "go10", "go11", "go12", "go1344"]}

    #FIX THE TEST FILE:
    #doesnt work yet because there are no actual go-terms in the test data...
    go_tree = read_go_tree("go-basic.obo")
    for gene in true_assignment:
        true_assignment[gene] = fix_go(true_assignment[gene], go_tree)

    #FIX THE PREDICTOR OUTPUT:
    for gene in training_assignment:
        training_assignment[gene] = fix_go(training_assignment[gene], go_tree)

    #VECTORIZE THE TEST AND PREDICTION FILES




    #start = time.time()
    #slice_gaf("mouse.gaf", "mouse_percent.gaf", dex, 90)
    #print("took:",  time.time() - start, "seconds")
    #start = time.time()
    #slice_gaf("mouse.gaf", "mouse_percent.gaf", dex, 90)
    #print("took:",  time.time() - start, "seconds")
    #start = time.time()
    #slice_gaf("mouse.gaf", "mouse_percent.gaf", dex, 90)
    #print("took:",  time.time() - start, "seconds")
    #start = time.time()
    #slice_gaf("mouse.gaf", "mouse_percent.gaf", dex, 90)
    #print("took:",  time.time() - start, "seconds")
    #print("done")
main()
