"""
Filtergaf removes the header of a gaf file (lines starting with !)
Also removes lines from the gaf file if it doesnt have an evidence code or domain.
"""

def filter_gaf(gaf_lines, evidence_codes, domains):
    number=0
    for determineheader in gaf_lines[0:200]:
        if determineheader[0] == "!":
            number += 1
    headfiltered_gaf = gaf_lines[number:]
    for index, line in enumerate(headfiltered_gaf):
        line_items = line.split("\t")
        if line_items[3] != "" or line_items[6] not in evidence_codes or line_items[8] not in domains or line_items[8] == "C":
            del headfiltered_gaf[index]
    return headfiltered_gaf
