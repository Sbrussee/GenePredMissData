import numpy as np

#Preferable input for the evaluator:
#The proteins should be rows and the GO-terms should be columns.
#If input differs, functions in the evaluator will need to correct this.

#Evaluator class:
class Evaluator:
    #Iniatior function,sets metrics to empty string in order to be able to
    #check if these metrics are already calculated.
    def __init__(self, true_annotation, pred_annotation, train_annotation, desired_metrics):
        #Set input files/lists
        #True (Y_true), Pred (Y_pred) > Need to be in np array format.
        self.true_annotation = true_annotation
        self.pred_annotation = pred_annotation
        #Set train annotation for calculating ic-scores per term.
        self.train_annotation = train_annotation
        #Variable that should define the desired metric(s)
        self.desired_metrics = desired_metrics
        #Determine number of terms and proteins.
        (self.num_of_pred_proteins, self.num_of_pred_go_terms) = np.shape(self.pred_annotation)
        (self.num_of_true_proteins, self.num_of_true_go_terms) = np.shape(self.true_annotation)
        (self.num_of_train_proteins, self.num_of_train_go_terms) = np.shape(self.train_annotation)
        #Set empty variables which should be determined by the class methods.
        #Inconsistency scores
        self.ic = ''
        #Remaining Uncertainty
        self.ru = ''
        #Missing information
        self.mi = ''
        #Semantic Distance
        self.sd = ''

    #Function to calculate the inconsistency scores.
    def get_ic(self):
        #check if the ic-scores exist already
        if len(self.ic) > 0:
            return self.ic
        #Make array for the inconsistency scores.
        ic_scores = np.zeros((self.num_of_train_go_terms,), float)
        for term_index in range(self.num_of_train_go_terms):
            #Get list of protein scores for the term
            proteins = self.pred_annotation[:,term_index]
            #Make list of 1-values with the length of total amount of proteins to use as denominator.
            min_list = np.ones(self.num_of_train_proteins,)
            #Loop through parents of term (parents are already in list for the protein)
            #Not entirely sure if necessary for our approach?
            for parent in self.pred_annotation[:,term_index]:
                #Set scores to divide to the lowest p-score.
                min_list = np.minimum(min_list, parent)
            #Check whether the protein scores and the division scores are higher than 0:
            if np.sum(proteins) > 0 and np.sum(min_list) > 0:
                #calculate p-values
                p_value = float(np.sum(proteins)) / float(np.sum(min_list))
                #Check whether p-values are possible.
                if p_value < 0.0 or p_value > 1.0:
                    print("Ain't working correctly")
                #Set inconsistency scores for each term
                ic_scores[term_index] = -1.0 * np.log2(p_value)
            #If any of the scores are 0, set the ic-score for the term to 0.
            else:
                ic_scores[term_index] = 0.0
        self.ic = ic_scores

    #Function for calculating remaining uncertainty
    def get_ru(self):
        #check if ru-scores already exist
        if len(self.ru) > 0:
            return self.ru
        #Make sure ic-scores have been calculated.
        if len(self.ic) == 0:
            self.ic = self.get_ic()
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

    def get_average_ru(self):
        #check whether ru-scores have been calculated.
        if len(self.ru) == 0:
            self.ru = self.get_ru()
        #if ru exists, return the mean of the scores.
        else:
            return np.mean(self.ru)

    #Function to calculate Missing Information scores for the proteins.
    def get_mi(self):
        #check if mi-scores already exist
        if len(self.mi) > 0:
            return self.mi
        #Make sure ic-scores have been calculated.
        if len(self.ic) == 0:
            self.ic = self.get_ic()
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

    def get_average_mi(self):
        #check whether mi-scores have been calculated.
        if len(self.mi) == 0:
            self.mi = self.get_mi()
        #if mi exists, return the mean of the scores.
        else:
            return np.mean(self.mi)

    #Function to calculate the Semantic Distance.
    def get_sd(self):
        #Check whether sd has already been calculated.
        if len(self.sd) > 0:
            return self.sd
        #Check whether ru and mi have been calculated.
        if len(self.ru) == 0:
            self.ru = self.get_ru()
        if len(self.get_mi) == 0:
            self.mi = self.get_mi()
        #Calculate semantic distance.
        self.sd = np.sqrt(self.ru ** 2 + self.get_mi ** 2)

