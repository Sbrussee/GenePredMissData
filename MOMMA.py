#!/usr/bin/env python3
import importlib
import random
from arguments import get_args
import time


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
    

def main():
    #argstore = get_args()
    dex = index_gaf("mouse.gaf", ["ND", "ISO", "IMP", "IDA", "EXP"])
    start = time.time()
    slice_gaf("mouse.gaf", "mouse_percent.gaf", dex, 90)
    print("took:",  time.time() - start, "seconds")
    start = time.time()
    slice_gaf("mouse.gaf", "mouse_percent.gaf", dex, 90)
    print("took:",  time.time() - start, "seconds")
    start = time.time()
    slice_gaf("mouse.gaf", "mouse_percent.gaf", dex, 90)
    print("took:",  time.time() - start, "seconds")
    start = time.time()
    slice_gaf("mouse.gaf", "mouse_percent.gaf", dex, 90)
    print("took:",  time.time() - start, "seconds")
    print("done")
main()
