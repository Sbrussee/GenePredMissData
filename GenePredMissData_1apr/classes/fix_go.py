import time

class Go_Fixer:
    def fix_go(self, termlist):
        for term in termlist:
            termlist[termlist.index(term)] = self.replace_obsolete_terms(term)
            try:
                parents = self.go_tree[term]
                while type(parents) == str:
                    parents = self.go_tree[parents]
            except KeyError:
                continue
            for pterm in parents:
                if not pterm in termlist and pterm != '':
                    termlist.append(pterm)
        return termlist

    """
    Parameters: self (class), term (String).
    
    This function replaces obsolete terms which aren't recognized as obsolete by the gaf file.
    A dictionary with obsolete terms and the replacement terms is made. If the term given
    to the function is a key in the dictionary, the term variable is replaced by the replacement
    term. The replacement term is returned.
    
    Returns: term (String) 
    """
    def replace_obsolete_terms(self, term):
        if term in self.obsolete_terms.keys():
            term = self.obsolete_terms[term]
        return term

    def __init__(self, filename):
        self.go_tree = {}
        self.obsolete_terms = {}
        with open(filename) as file:
            id, name, term, replace, obsolete, relation = "", \
            "", [], "", False, []
            lines = file.readlines()
            for line in lines:
                line = line.split(": ")
                if line[0] == "id":
                    id = line[1].strip()
                if line[0] == "replaced_by":
                    replace = line[1].strip()
                    self.obsolete_terms[id] = replace
                if line[0] == "alt_id":
                    self.obsolete_terms[line[1].strip()] = id
                if line[0] == 'namespace':
                    name = line[1].strip()
                if line[0] == "is_obsolete" and line[1].strip() == "true":
                    obsolete = True
                if line[0] == "is_a":
                    if len(line[1].split("!")[0].strip().split(":")) > 1:
                        term.append(line[1].split("!")[0].strip())
                if line[0] == "relationship":
                    rel = line[1].strip().split(" ")
                    if rel[0] in ["part_of", "negatively_regulates",
                                  "positively_regulates", "regulates"]:
                        term.append(rel[1])
                if line[0] == "\n" and name != "":
                    if replace != "":
                        if id in self.go_tree:
                            self.go_tree[id] = self.go_tree[id] + term
                        else:
                            self.go_tree[id] = term
                    elif not obsolete:
                        if id in self.go_tree:
                            self.go_tree[id] = self.go_tree[id] + term
                        else:
                            self.go_tree[id] = term
                    id, name, term, replace, obsolete = "", "", [], "", False
            del lines

    def get_go_tree(self):
        return self.go_tree

