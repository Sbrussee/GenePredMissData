import time

def fix_go(termlist, go_tree):
    list = []
    for term in termlist:
        if term in go_tree:
            list.append(term)
    return list

def read_go_tree(filename, proces):
    go_tree = {}
    uniek = {}
    getal = 0
    with open(filename) as file:
        id, name, term, replace, obsolete, relation = "", "", [], "", False, []
        lines = file.readlines()
        for line in lines:
            line = line.split(": ")

            if line[0] == "id":
                id = line[1].strip()

            if line[0] == "replaced_by":
                replace = line[1].strip()

            if line[0] == 'namespace':
                name = line[1].strip()

            if line[0] == "is_obsolete" and line[1].strip() == "true":
                obsolete = True

            if line[0] == "is_a":
                if len(line[1].split("!")[0].strip().split(":")) > 1:
                    term.append(line[1].split("!")[0].strip())

            if line[0] == "relationship":
                rel = line[1].strip().split(" ")
                if rel[0] in ["part_of", "negatively_regulates", "positively_regulates", "regulates"]:
                    term.append(rel[1])
            if proces == name:
                if line[0] == "\n" and name != "":
                    if "GO" in id:
                        if id not in uniek:
                            uniek[id] = getal
                            getal += 1
                    if replace != "":
                        go_tree[id] = term
                    elif not obsolete:
                        go_tree[id] = term
                    id, name, term, replace, obsolete = "", "", [], "", False
        del lines
    return go_tree, uniek

