import numpy as np
import matplotlib.pyplot as plt
import datetime
import collections
from random import randint
import pandas as pd

"""
The Plotter class will plot the metrics generated by the Evaluator class on all
specified missing data fractions. The class requires an array containing the
missing data fractions and an array containing the average IC-scores (or other scores?)
for each missing data fraction.
"""
class Plotter:
    def __init__(self):
        self.frac_of_miss_array = []
        self.dictarray = []

    """
    Add_score will add fraction data to the frac_of_miss_array list
    Add score will also add a dictionary with the technique as key and corresponding value used for plotting.
    For example{'f1-score',10} to the dictarray, this will be used in plot performance.
    """
    def add_score(self, fraction, mean):
        self.frac_of_miss_array.append(fraction)
        self.dictarray.append(mean)

    """
    Plot_performance is able to plot multiple times depending on the amount of unique keys in the dict_array
    This will count the amount of fractions and plot the mean and standard deviation for each fraction
    Plotter will also give the corresponding x-as and y-axis names to the corresponding technique used
    This plotter is able to combine results from multiple techniques.
    Implemented line-type and line coloring with config file 7pm 13-06-2019
    """
    def plot_performance(self, title, totalruns, extrainfo,date):
        uniquelist = []
        for key in self.dictarray[0]:
            if key not in uniquelist:
                uniquelist.append(key)

        totallist = np.array_split(self.frac_of_miss_array, len(totalruns))
        extratotallist = np.array_split(self.dictarray, len(totalruns))
        color = [x[0] for x in extrainfo]
        type = [y[1] for y in extrainfo]
        print("uniquelist:", uniquelist)
        for value in uniquelist:
            print("Value:", value)
            dataframeus = pd.DataFrame(columns=['means', 'stdevs', 'methods', 'fractions'])
            for (i, firstfrac, firstdict) in zip(totalruns, totallist, extratotallist):
                print(i, firstfrac, firstdict)
                newarray = [d[value] for d in firstdict]
                fractions = sorted(set(firstfrac))
                listf = list(firstfrac)
                amount_of_runs = listf.count(100)
                means = {}
                stdevs = {}
                for round in range(0,len(firstfrac),amount_of_runs):
                    acround = firstfrac[round]
                    means[acround] = np.mean(newarray[round:round+amount_of_runs])
                    stdevs[acround] = np.std(newarray[round:round+amount_of_runs])
                means = collections.OrderedDict(sorted(means.items()))
                stdevs = collections.OrderedDict(sorted(stdevs.items()))
                vs = [{'means': mean,
                      'stdevs': stdev,
                      'fractions':fraction,
                      'methods': i} for mean, stdev, fraction in zip(list(means.values()),
                                                             list(stdevs.values()),
                                                             fractions)]
                dataframeus = dataframeus.append(vs, ignore_index=True)
            reformed = dataframeus.pivot('fractions','methods')
            for number, valueas in enumerate(totalruns):
                if color[number] != '*':
                    plt.errorbar(reformed.index,reformed['means'][valueas],yerr=reformed['stdevs'][valueas],
                        color=color[number],fmt='',linestyle=type[number], capsize=4)
                else:
                    plt.errorbar(reformed.index, reformed['means'][valueas], yerr=reformed['stdevs'][valueas],
                                 capsize=4)
            plt.legend(totalruns)
            plt.xticks(fractions)  # location, labels
            plt.xlim(fractions[0]-0.5, fractions[-1]+0.5)
            plt.title(title)
            plt.ylabel(value.replace("_", " "))
            plt.xlabel('fractions of data')
            plt.gca().invert_xaxis()
            plt.grid(True)
            writeout = title + date + value 
            plt.savefig(writeout)
            plt.close()
