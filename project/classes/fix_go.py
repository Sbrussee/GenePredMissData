import time

def fix_go(termlist, go_tree):
    for term in termlist:
        try:
            parents = go_tree[term]
            while type(parents) == str:
                parents = go_tree[parents]
        except KeyError:
            continue
        for pterm in parents:
            if not pterm in termlist and pterm != '':
                termlist.append(pterm)
    return termlist

def read_go_tree(filename):
    go_tree = {}
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

            if line[0] == "\n" and name != "":
                if replace != "":
                    if id in go_tree.keys():
                        go_tree[id] = go_tree[id] + term
                    else:
                        go_tree[id] = term
                elif not obsolete:
                    if id in go_tree.keys():
                        go_tree[id] = go_tree[id] + term
                    else:
                        go_tree[id] = term

                id, name, term, replace, obsolete = "", "", [], "", False
        del lines
    return go_tree

