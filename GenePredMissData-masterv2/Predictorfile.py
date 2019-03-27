import json

#This Class converts a file containing uniprotKB to a dictionary
#Containing uniprotKB codes with the corresponding GO:id's
#This class needs a gaf file (f.a. mouse or rat gaf file containing uniprot id's and go id's)
#And a file containing the uniprotKB id's

class Predictor:
    def __init__(self):
        #self.method = method
        self.newlist = []
        self.dictionaryforwrite = dict()
        #if self.method == blastgo(gaffiletype):



    def makelist(self, list):
        self.newlist = list

    #This function will create the dictionary and add GO:id codes to the corresponding uniprotKB code
    def blastgo(self, gaffiletype):
        with open(gaffiletype, 'r') as gaf:
            for line in gaf:
                if line[0] != '!':
                    compareline = line.strip().split('\t')
                    strs = list(filter(None, compareline))
                    for xs in self.newlist:
                        if xs == strs[1]:
                            if 'GO:' in strs[3]:
                                if xs in self.dictionaryforwrite:
                                    self.dictionaryforwrite[xs].append(strs[3])
                                else:
                                    self.dictionaryforwrite[xs] = [strs[3]]
                            elif 'GO:' in strs[4]:
                                if xs in self.dictionaryforwrite:
                                    self.dictionaryforwrite[xs].append(strs[4])
                                    pass
                                else:
                                    self.dictionaryforwrite[xs] = [strs[4]]
                                    pass
        return self.dictionaryforwrite