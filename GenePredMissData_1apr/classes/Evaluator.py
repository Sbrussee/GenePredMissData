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
    def __init__(self, true_annotation, pred_annotation, evaluators, dtype=[]):
        # Set the input files/lists
        # True (Y_true), pred (Y_pred) > Need to be in np vector format.
        self.true_annotation = true_annotation
        self.pred_annotation = pred_annotation

        self.evaluators = evaluators

        # Determine number of terms and proteins.
        (self.num_of_pred_proteins, self.num_of_pred_go_terms) = self.pred_annotation.shape
        (self.num_of_true_proteins, self.num_of_true_go_terms) = self.true_annotation.shape

        # Set empty np-arrays which should be determined by the class methods.
        empty_array = np.empty((self.num_of_true_proteins))

        # F1-scores
        self.f1 = empty_array

        # Precision-scores
        self.prec = empty_array

        # R UM
        self.ru = empty_array

        # Missing:
        self.mi = empty_array

        # Semantic distance
        self.sd = empty_array

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

 #Function for calculating remaining uncertainty
    def get_ru(self):
        #check if ru-scores already exist
        if np.count_nonzero(self.ru) > 0:
            return self.ru
        #Make array for ru-values
        ru_scores = np.zeros((self.num_of_true_proteins), float)
        #loop through proteins in y-true.
        for prot_index in range(self.num_of_true_proteins):
            go_pred = self.pred_annotation[prot_index,:]
            go_true = self.true_annotation[prot_index,:]
            #Get the terms for which the predicted value was 0, but the true value is 1 (false negatives).
            fn_terms = np.intersect1d(np.where(go_true == 1), np.where(go_pred == 0))

            #loop through false negative terms.
            for fn_term_index in fn_terms:
                #Add the false negative term ic-scores to the ru-score for the protein.
                ru_scores[prot_index] += self.ic[fn_term_index]
        self.ru = ru_scores
        return self.ru

    def get_average_ru(self):
        #check whether ru-scores have been calculated.
        if np.count_nonzero(self.ru) > 0:
            self.ru = self.get_ru()
            return np.mean(self.ru)
        #if ru exists, return the mean of the scores.
        else:
            return np.mean(self.ru)

    #Function to calculate Missing Information scores for the proteins.
    def get_mi(self):
        #check if mi-scores already exist
        if np.count_nonzero(self.mi) > 0:
            return self.mi
        #Make array for ru-values
        mi_scores = np.zeros((self.num_of_true_proteins), float)
        #loop through proteins in y-true.
        for prot_index in range(self.num_of_true_proteins):
            go_pred = self.pred_annotation[prot_index,:]
            go_true = self.true_annotation[prot_index,:]
            #Get the terms for which the predicted value was 1, but the true value is 0 (false positives).
            fp_terms = np.intersect1d(np.where(go_true == 0), np.where(go_pred == 1))
            #loop through false positive terms.
            for fp_term_index in fp_terms:
                #Add the false positive term ic-scores to the mi-score for the protein.
                mi_scores[prot_index] += self.ic[fp_term_index]
        self.mi = mi_scores
        return self.mi

    def get_average_mi(self):
        #check whether mi-scores have been calculated.
        if np.count_nonzero(self.mi) > 0:
            self.mi = self.get_mi()
            return np.mean(self.mi)
        #if mi exists, return the mean of the scores.
        else:
            return np.mean(self.mi)

    #Function to calculate the Semantic Distance.
    def get_sd(self):
        #Check whether sd has already been calculated.
        if np.count_nonzero(self.sd) > 0:
            return self.sd
        #Check whether ru and mi have been calculated.
        if len(self.ru) == 0:
            self.ru = self.get_ru()
        if len(self.mi) == 0:
            self.mi = self.get_mi()
        #Calculate semantic distance.
        self.sd = np.sqrt(self.ru ** 2 + self.mi ** 2)
        return self.sd
















