import json

#This Class converts a file containing uniprotKB to a dictionary
#Containing uniprotKB codes with the corresponding GO:id's
#This class needs a gaf file (f.a. mouse or rat gaf file containing uniprot id's and go id's)
#And a file containing the uniprotKB id's

class Predictor:
    def __init__(self, method, arg1=0, arg2=0):
        self.method = method
        if self.method == "blast":
            self.newlist = arg1

    #This function will create the dictionary and add GO:id codes to the corresponding uniprotKB code
    def blast(self, gaf_file):
        if type(self.newlist) != list:
            print("Error: You have not given the BLAST-method the Uniprot list.")
        self.pred_dict = dict()
        for line in gaf_file:
            if line[0] != '!':
                compareline = line.strip().split('\t')
                strs = list(filter(None, compareline))
                for uniprot_code in self.newlist:
                    if uniprot_code == strs[1]:
                        if 'GO:' in strs[3]:
                            if uniprot_code in self.pred_dict:
                                self.pred_dict[uniprot_code].append(strs[3])
                            else:
                                self.pred_dict[uniprot_code] = [strs[3]]
                        elif 'GO:' in strs[4]:
                            if uniprot_code in self.pred_dict:
                                self.pred_dict[uniprot_code].append(strs[4])
                                pass
                            else:
                                self.pred_dict[uniprot_code] = [strs[4]]
                                pass
        return self.pred_dict