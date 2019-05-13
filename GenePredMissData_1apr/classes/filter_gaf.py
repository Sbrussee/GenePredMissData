def filter_gaf(gaf_lines, evidence_codes, domains):
    headfiltered_gaf = gaf_lines[12:]
    for index, line in enumerate(headfiltered_gaf):
        line_items = line.split("\t")
        if line_items[3] != "" and line_items[6] not in evidence_codes and line_items[8] not in domains:
            del headfiltered_gaf[index]
    return headfiltered_gaf
