import time

def read_go_tree(filename):
    go_tree = {}
    with open(filename) as file:
        name, term, replace, obsolete = "", [], "", False
        lines = file.readlines()
        for line in lines:
            line = line.split(": ")
            if line[0] == "replaced_by":
                replace = line[1].strip()
            if line[0] == "id":
                name = line[1].strip()
            if line[0] == "is_obsolete" and line[1] == "true\n":
                obsolete = True
            if line[0] == "is_a":
                term.append(line[1].split("!")[0].strip())
            if line[0] == "relationship":
                rel = line[1].split(" ")
                if rel[0] in ["part_of", "negatively_regulates",
                              "positively_regulates", "regulates"]:
                    term.append(rel[1])
            if line[0] == "\n" and name != "":
                if replace != "":
                    go_tree[name] = replace
                elif not obsolete:
                    go_tree[name] = term
                name, term, replace, obsolete = "", [], "", False
        del lines
    return go_tree


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


def main():
    go_tree = read_go_tree("go-basic.obo")
    times = time.time()
    for x in range(500):
        res = fix_go(["GO:2001317"], go_tree)
    print(time.time() - times)
    print(res)
    

if __name__ == "__main__":
    main()
