import time

def read_go_tree(filename):
    go_tree = {}
    with open(filename) as file:
        name, term = "", []
        lines = file.readlines()
        for line in lines:
            line = line.split(": ")
            if line[0] == "id":
                name = line[1].strip()
            if line[0] == "is_a":
                term.append(line[1].split("!")[0].strip())
            if line[0] == "\n" and name != "":
                go_tree[name] = term
                name, term = "", []
        del lines
    return go_tree


def fix_go(termlist, go_tree):
    for term in termlist:
        parents = go_tree[term]
        for pterm in parents:
            if not pterm in termlist and pterm != '':
                termlist.append(pterm)
    return termlist


def main():
    go_tree = read_go_tree("go-basic.obo")
    times = time.time()
    res = fix_go(["GO:0000257"], go_tree)
    print(time.time() - times)
    print(res)
    

if __name__ == "__main__":
    main()
