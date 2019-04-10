import numpy as np
import matplotlib.pyplot as plt

#The Plotter class will plot the metrics generated by the Evaluator class on all
#specified missing data fractions. The class requires an array containing the
#missing data fractions and an array containing the average IC-scores (or other scores?)
#for each missing data fraction.
class Plotter:
    def __init__(self):
        self.frac_of_miss_array = []
        self.performance_array = []
        self.stdev_array = []

    def add_score(self, fraction, mean, stdev):
        self.frac_of_miss_array.append(fraction)
        self.performance_array.append(mean)
        self.stdev_array.append(stdev)

    def plot_performance(self):
        fractions = sorted(set(self.frac_of_miss_array))
        amount_of_runs = self.frac_of_miss_array.count(100)
        means = dict.fromkeys(fractions)
        stdevs = dict.fromkeys(fractions)
        for index, fraction in enumerate(self.frac_of_miss_array):
            means[fraction] = np.mean(self.performance_array[index-amount_of_runs:index])
            stdevs[fraction] = np.std(self.performance_array[index-amount_of_runs:index])

        means = np.asarray(list(means.values())[::-1])
        stdevs = np.asarray(list(stdevs.values())[::-1])
        plt.errorbar(np.arange(len(fractions)), means, stdevs, lw=3, fmt='ok')
        plt.xticks(np.arange(len(fractions)), [100 - x for x in fractions[::-1]])
        plt.plot(means)
        plt.ylabel('Performance score')
        plt.xlabel('Percentage of missing data')
        plt.title("PFP-model performance under varying missing data fractions")
        plt.savefig('performance_plot.png')
        plt.show()
