import numpy as np

# Function that takes the true annotation files and retrieves the uniprotKBs + GO-terms dictionairy
def parse_true_annotation(annotation_lines):
    # Create dictionaire for the annotation
    true_annotation_dict = dict()
    # Loop through the annotation file
    for line in annotation_lines:
        # Check which line is a documentation line
        if line.startswith("!") == False:
            # Split the line into sections
            line_items = line.split("\t")
            # Get the protein section
            protein = line_items[1]
            # Check if the GO-term is valid
            if line_items[3] != "NOT":
                # Check whether protein code is already in the dictionaire
                if protein not in true_annotation_dict.keys():
                    # Create a empty list for the GO-terms if so.
                    true_annotation_dict[protein] = []
                    true_annotation_dict[protein].append(line_items[4])
                # If not, add the go-annotation to the protein in question.
                else:
                    true_annotation_dict[protein].append(line_items[4])

    return true_annotation_dict