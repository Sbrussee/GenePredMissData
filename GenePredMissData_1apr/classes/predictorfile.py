import json

#This Class converts a file containing uniprotKB to a dictionary
#Containing uniprotKB codes with the corresponding GO:id's
#This class needs a gaf file (f.a. mouse or rat gaf file containing uniprot id's and go id's)
#And a file containing the uniprotKB id's

class Predictor:
    def __init__(self, method, arg1=0, arg2=0):
        self.method = method
        if self.method == "blast":
            self.uniprot_codes = arg1

    #This function will create the dictionary and add GO:id codes to the corresponding uniprotKB code
    def blast(self, annotation_lines):
        if type(self.uniprot_codes) != list:
            print("Error: You have not given the BLAST-method the Uniprot list.")
        true_annotation_dict = dict()
        for line in annotation_lines:
            # Check which line is a documentation line
            if line.startswith("!") == False:
                # Split the line into sections
                line_items = line.split("\t")
                # Get the protein section
                protein = line_items[7]
                # Check if there is a UniProtKB link in the section if the GO-term is valid
                if "UniProtKB:" in protein and line_items[3] != "NOT":
                    # Get the UniprotKB code for the protein
                    protein = protein.split("UniProtKB:")[1][0:6]
                    # Check whether protein code is already in the dictionaire
                    if protein not in true_annotation_dict.keys():
                        # Create a empty list for the GO-terms if so.
                        true_annotation_dict[protein] = []
                    # If not, add the go-annotation to the protein in question.
                    else:
                        true_annotation_dict[protein].append(line_items[4])

        # Filter empty go-term list from the dictionary.
        # true_annotation_dict = dict((key, val) for key, val in true_annotation_dict.items() if val)
        return true_annotation_dict
