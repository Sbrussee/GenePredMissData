import warnings
import numpy as np
import sklearn.metrics as metrics
from sklearn.exceptions import UndefinedMetricWarning

warnings.filterwarnings("ignore", category=UndefinedMetricWarning)

"""
Evaluator Class:

The Evaluator class takes the predicted go-terms predicted by the Predictor class and
the true go-terms taken from a gaf-file and evaluates the prediction performance of each predicted annotation
by looking at the true annotation found in the gaf-file. The evluator only calculates metrics specified by the user
in the command line. The Evaluator will return the mean of the specified metric for each predicted annotation.
"""

class Evaluator:
    """
    Parameters:
        - true_annotation: 2D-numpy array [proteins; go-terms] with the protein annotations taken from the gaf file.
        - pred_annotation: 2D-numpy array [proteins; go-terms] with the predicted protein annotations from the predictor
        - evaluators: list of the specified performance metrics as specified by the user.
        - dtype: datatype which is in the true_annotation and pred_annotation vectors.

    The initiator function takes the predicted annotation, the true annotation and the specified evaluation metrics.
    The function then determines the number of go-terms and proteins in each set by looking at the vector shape of the
    annotation variables. (number of rows: number of proteins, number of columns: number of go-terms) The function
    continues by making an empty numpy-array which is as long as the number of proteins in the true annotation. This
    empty array is saved in the class variables for each metric that can be calculated by the evaluator. The performance
    metric for each protein prediction will be saved in these empty arrays.
    """
    def __init__(self, true_annotation, pred_annotation, evaluators, dtype=''):
        # Set the input files/lists
        # True (Y_true), pred (Y_pred) > Need to be in np vector format.
        self.true_annotation = true_annotation
        self.pred_annotation = pred_annotation

        self.evaluators = evaluators
        self.dtype = dtype

        # Determine number of terms and proteins.
        (self.num_of_pred_proteins, self.num_of_pred_go_terms) = self.pred_annotation.shape
        (self.num_of_true_proteins, self.num_of_true_go_terms) = self.true_annotation.shape

        # Set empty np-arrays which should be determined by the class methods.
        empty_array = np.empty((self.num_of_true_proteins))

        # F1-scores
        self.f1 = empty_array

        # Precision-scores
        self.prec = empty_array

        # Average precision scores
        self.avprec = empty_array

    """
    The get_evaluation function makes a dictionary of the specified evaluation performance metrics as keys and checks
    which metrics are in this dictionary. If a given metric is in the dictionary, the function will call the function
    for this metric and the mean score will be saved as a value for the metric key. The function will return the
    dictionary which now contain the metrics as keys and the mean performance scores as values.
    
    returns:
        - evaluaton_dict: dictionary with specified metrics as keys and mean performance scores as values.
    """
    def get_evaluation(self):
        evaluation_dict = dict.fromkeys(self.evaluators)
        if 'precision' in self.evaluators:
            evaluation_dict['precision'] = self.get_precision()
        if 'average_precision' in self.evaluators:
            evaluation_dict['average_precision'] = self.get_average_precision()
        if 'f-score' in self.evaluators:
            evaluation_dict['f-score'] = self.get_f1()
        return evaluation_dict

    """
    The get_precision function will loop through the proteins in the true annotation dataset and take the true
    annotation- and the predicted annotation for a protein at a certain index position. The function calculates the
    precision score for this protein and saved it in the protein index position in the empty array initialized in the
    initializer function of the Evaluator class. After looping through the proteins, the function will return the mean
    of the calculated precision scores.
    
    returns:
        - self.prec.mean(): mean of the precision scores calculated for each protein (each index) of the true annotation
                            dataset. 
    """
    def get_precision(self):
        for index in range(self.num_of_true_proteins):
            true_row = self.true_annotation[index].toarray()[0]
            pred_row = self.pred_annotation[index].toarray()[0]
            self.prec[index] = metrics.precision_score(true_row, pred_row)
        return self.prec.mean()
    """
    The get_average_precision function will loop through the proteins in the true annotation dataset and take the true
    annotation- and the predicted annotation for a protein at a certain index position. The function calculates the
    average precision score for this protein and saved it in the protein index position in the empty array initialized
    in the initializer function of the Evaluator class. After looping through the proteins, the function will return
    the mean of the calculated average precision scores.
    
    returns:
        - self.avprec.mean(): mean of the average precision scores calculated for each protein (each index) of the true
         annotation dataset. 
    """
    def get_average_precision(self):
        for index in range(self.num_of_true_proteins):
            true_row = self.true_annotation[index].toarray()[0]
            pred_row = self.pred_annotation[index].toarray()[0]

            self.avprec[index] = metrics.average_precision_score(true_row, pred_row)
        return self.avprec.mean()
    """
    The get_f1 function loops through the proteins (indexes) in the true annotation dataset and takes the predicted- and
    true annotation for a protein at an index. It then feeds these annotations to the f1_score function which
    calculates the f1-score for the protein prediction at the index. The f1-score is saved at the protein index in
    the f1-array initialized as an empty array in the initializer function. The function returns the mean of the
    calculated f1-scores.
    
    returns:
        - f1.mean(): mean of the calculated f1-scores of all the protein predictions.
    """
    def get_f1(self):
        for index in range(self.num_of_true_proteins):
            true_row = self.true_annotation[index].toarray()[0]
            pred_row = self.pred_annotation[index].toarray()[0]
        
            prot_f1 = metrics.f1_score(true_row, pred_row)
            self.f1[index] = prot_f1
        return self.f1.mean()