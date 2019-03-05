import numpy as np
import sklearn.metrics as metrics
import sklearn.multiclass as multiclass
import sklearn.preprocessing as preprocessing
import matplotlib.pyplot as plt

#Preferable input for the evaluator:
#List of real GO-terms and list of pred GO terms for each instance.
#If input differs, functions in the evaluator will correct this.

#Evaluator class:
class Evaluator:
    #Iniatior function,sets metrics to empty string in order to be able to
    #check if these metrics are already calculated.
    def __init__(self, real_annotation, pred_annotation):
        #Set input files/lists
        self.real_annotation = real_annotation
        self.pred_annotation = pred_annotation
        #Set metrics.
        self.average_accuracy = ''
        self.average_precision = ''
        self.average_recall = ''
        self.average_f_measure = ''
        self.max_f_measure = ''
        #Set binary inputs.
        self.binary_real_annotation = ''
        self.binary_pred_annotation = ''


    #Function usable to get input in proper format.
    #def get_correct_input_format(self):
    #   correct_real = []
    #   for line in real_input_file:
    #       correct_real.append(line.split(" ")[1]) #Would be a list of real GO-terms
    #   correct_pred = []
    #   for line in pred_input_file:
    #       correct_pred.append(line.split(" ")[1]) #Would be a list of pred GO-terms
    #   self.real_annotation = correct_real
    #   self.pred_annotation = correct_pred

    #Standard accuracy method.
    def get_accuracy(self):
        #Check whether metric is already calculated.
        if len(self.average_accuracy) == 0:
            #Calculate metric and return it.
            return metrics.accuracy_score(self.real_annotation, self.pred_annotation)
        else:
            #Return previously calculated metric.
            return self.average_accuracy

    #Precision method, calculates average precision from a single function.
    def get_precision(self):
        #Check whether metric is already calculated.
        if len(self.average_precision) == 0:
            #Calculate metric and return it.
            return metrics.average_precision_score(self.real_annotation, self.pred_annotation)
        else:
            #Return previously calculated metric.
            return self.average_precision

    #Recall method
    def get_recall(self):
        #Check whether metric is already calculated.
        if len(self.average_recall) == 0:
            #Calculate metric and return it.
            return metrics.recall_score(self.real_annotation, self.pred_annotation)
        else:
            #Return previously calculated metric.
            return self.average_recall

    #F-measure method, f-max needs to be added.
    def get_f(self):
        #Check whether metric is already calculated.
        if len(self.average_f_measure) == 0:
            #Calculate metric and return it.
            return metrics.f1_score(self.real_annotation, self.pred_annotation)
        else:
            #Return previously calculated metric.
            return self.f

    #Binarize-method in order for data to be applicable in ROC-curve methods.
    def binarize_input(self):
        #Check whether input is already binarized:
        if len(self.binary_real_annotation) == 0:
            #Binarize real annotation and predicted annotation.
            self.binary_real_annotation = preprocessing.binarize(self.real_annotation)
            self.binary_pred_annotation = preprocessing.binarize(self.pred_annotation)
        else:
            #Do nothing if input was already binarized.
            pass

    #INPUT NEEDS TO BE BINARIZED IN ORDER TO WORK FOR MULTI-LABEL CLASSIFICATION!
    #GO-centric ROC evalution:
    #def get_go_roc_curves:
    #
    #
    #Protein-centric ROC evaluation:
    #def get_protein_roc_curves:
    #
    #

    def get_all_evaluations(self):
        #Return all available metrics by calling their respective functions:
        return "Average accuracy:\t%d\n" \
               "Average Precision:\t%d\n" \
               "Average Recall:\t%d\n" \
               "Average F-measure:\t%d\n" \
               % (self.get_accuracy(), self.get_precision(),
                  self.get_recall(), self.get_f())