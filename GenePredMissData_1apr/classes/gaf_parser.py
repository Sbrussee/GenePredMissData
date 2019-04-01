import numpy as np

# Function that takes the true annotation files and retrieves the uniprotKBs + GO-terms dictionary
def gaf_parse(annotation_lines):
    # Create dictionary for the annotation
    annotation_dict = dict()
    # Loop through the annotation file
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
                if protein not in annotation_dict.keys():
                    # Create a empty list for the GO-terms if so.
                    annotation_dict[protein] = []
                # If not, add the go-annotation to the protein in question.
                else:
                    annotation_dict[protein].append(line_items[4])
    return annotation_dict
