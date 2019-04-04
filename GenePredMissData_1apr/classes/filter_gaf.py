def filter_gaf(gaf_lines, evidence_codes=['EXP', 'IDA', 'IPI', 'IMP', 'IGI', 'IEP',
                  'HTP', 'HDA', 'HMP', 'HGI', 'HEP', 'IBA',
                  'IBD', 'IKR', 'IRD', 'ISS', 'ISO', 'ISA', 'ISM',
                  'IGC', 'RCA', 'TAS', 'NAS', 'IC', 'ND',
                  'IEA']):
    headfiltered_gaf = gaf_lines[12:]
    for index, line in enumerate(headfiltered_gaf):
        line_items = line.split("\t")
        if line_items[3] != "" or line_items[6] not in evidence_codes:
            del headfiltered_gaf[index]
    return headfiltered_gaf