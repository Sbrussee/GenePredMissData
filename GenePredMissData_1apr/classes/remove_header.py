def remove_header(gaf_lines):
    for index, line in enumerate(gaf_lines):
        if line.startswith("!"):
            del gaf_lines[index]
        else:
            return gaf_lines