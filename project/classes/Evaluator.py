import numpy as np
import sklearn.metrics as metrics

# Preferable input for the evaluator:
# The proteins should be rows and the GO-terms should be columns.
# If input differs, function in the evaluator will need to correct this.

# Arrays with the performance metrics can be retrieved from the class, these should be put in
# arrays and then be given to the plotter.

class Evaluator:
    # Initiator function, sets, metrics to empty string in order to be able to check if these metrics are already calc
    # Check if these metrics are already calculated.
    def __init__(self, true_annotation, pred_annotation):
        # Set the input files/lists
        # True (Y_true), pred (Y_pred) > Need to be in np vector format.
        self.true_annotation = true_annotation
        self.pred_annotation = pred_annotation
        # Set given vector of term IC-scores.
        # self.ic = termICs.
        # Determin number of terms and proteins.
        (self.num_of_pred_proteins, self.num_of_pred_go_terms) = self.pred_annotation.shape
        (self.num_of_true_proteins, self.num_of_true_go_terms) = self.true_annotation.shape

        # Set empty np-arrays which should be determined by the class methods.
        empty_array = np.zeros((self.num_of_true_proteins))

        # F1-scores
        self.f1 = empty_array

        # R UM
        self.ru = empty_array

        # Missing:
        self.mi = empty_array

        # Semantic distance
        self.sd = empty_array

    def get_f1(self):
        # Check if f1 already exist:
        if np.count_nonzero(self.f1) > 0:
            return self.f1

        for index in range(self.num_of_true_proteins):

            true = self.true_annotation[index, ][np.where(self.true_annotation[index, ] == 1)]
            pred = self.pred_annotation[index,][np.where(self.true_annotation[index,] == 1)]

            true1 = self.true_annotation[index, ][np.intersect1d(np.where(self.true_annotation[index,] == 0), np.where(self.pred_annotation[index, ] == 1))]
            pred1 = self.pred_annotation[index,][np.intersect1d(np.where(self.true_annotation[index,] == 0), np.where(self.pred_annotation[index,] == 1))]

            true_array = np.hstack((true, true1))
            pred_array = np.hstack((pred, pred1))

            if len(true_array) > 1:
                prot_f1  = metrics.f1_score(true_array, pred_array)
                self.f1[index] = prot_f1
        return self.f1

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
















