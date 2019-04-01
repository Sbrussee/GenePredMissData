import numpy as np
import matplotlib.pyplot as plt

#The Plotter class will plot the metrics generated by the Evaluator class on all
#specified missing data fractions. The class requires an array containing the
#missing data fractions and an array containing the average IC-scores (or other scores?)
#for each missing data fraction.
class Plotter:
    def __init__(self):
        self.frac_of_miss_array = []
        self.performance_array =[]

    def add_score(self, frac_of_miss_array, performance_array):
        self.frac_of_miss_array.append(frac_of_miss_array)
        self.performance_array.append(performance_array)

    # Function to plot the model performance against the fraction of missing data.
    def plot_performance(self):
        perf_plot, perf_ax = plt.subplots()
        perf_ax.plot(self.frac_of_miss_array, self.performance_array)
        plt.xlabel("Percentage of prediction data")
        plt.ylabel("Model performance")
        plt.title("PFP-model performance under varying missing data fractions")
        plt.show()