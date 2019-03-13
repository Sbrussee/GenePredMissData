import numpy as np
def main():
    # A training example dataset
    true_assignment = {0:["go1", "go2", "go3", "go4", "go5", "go6", "go7", "go8", "go9", "go10", "go11", "go12", "go13"],
                       1:["go14", "go15", "go16", "go17", "go22", "go33", "go11", "go8", "go9", "go112", "go119", "go159", "go13"],
                       2:["go1", "go2", "go35", "go4", "go5", "go56", "go755", "go8", "go99", "go10", "go11", "go12", "go133"],
                       3:["go1", "go12", "go3", "go44", "go54", "go20", "go17", "go98", "go93", "go10", "go11", "go12", "go13"],
                       4:["go1", "go2", "go3", "go4", "go5", "go6", "go7", "go8", "go9", "go10", "go11", "go12", "go1344"]}

    # A test example dataset
    gen1 = ["go1", "go2", "go3", "go4", "go5", "go6", "go7", "go8", "go9", "go10", "go11", "go12", "go13"]
    gen2 = ["go14", "go15", "go16", "go17", "go22", "go33", "go11", "go8", "go9", "go112", "go119", "go159", "go13"]
    gen3 = ["go1", "go2", "go35", "go4", "go5", "go56", "go755", "go8", "go99", "go10", "go11", "go12", "go133"]
    gen4 = ["go1", "go12", "go3", "go44", "go54", "go20", "go17", "go98", "go93", "go10", "go11", "go12", "go13"]
    gen5 = ["go1", "go2", "go3", "go4", "go5", "go6", "go7", "go8", "go9", "go10", "go11", "go12", "go1344"]
    genen = [gen1, gen2, gen3, gen4, gen5]

    # Maak test data evaluator input
    go_assignment = count_terms(genen)
    input_test_evaluator = make_input(next(go_assignment), next(go_assignment))
    print("test array:")
    print(next(input_test_evaluator))

    # Make training data evaluator input
    true_terms = count_true_terms(true_assignment)
    input_training_evaluator = make_input(true_assignment, next(true_terms))
    print("\ntraining true array:")
    print(next(input_training_evaluator))

def count_true_terms(true_assignment):
    go_terms = []
    for terms in true_assignment.values():
        for term in terms:
            if term not in go_terms:
                go_terms.append(term)
    yield go_terms

def make_input(go_assignment, go_terms):
    # len_go_assignment: all genes
    # len_go_terms: all unique go terms
    len_go_assignment = len(go_assignment)
    len_go_terms = len(go_terms)

    # input_evaluator: A numpy array with the length of all unique go terms and the rows all genes.
    input_evaluator = np.zeros((len_go_assignment, len_go_terms), dtype="int")

    # iterative: Change all zeros to one, if the go-term is assigned to a gene(rows)
    for gen, terms in go_assignment.items():
        for a in terms:
            index = go_terms.index(a)
            input_evaluator[gen, index] = 1
    yield input_evaluator

def count_terms(genen):
    # go_assignment: dictionaire to save for each gene all go terms
    # go_terms: list to save all unique go terms
    go_assignment = {}
    go_terms = []

    # iteratie: Save all unique go terms and dor each gene all go terms.
    for getal, gen in enumerate(genen):
        go_assignment[getal] = gen
        for terms in gen:
            if terms not in go_terms:
                go_terms.append(terms)
    yield go_assignment
    yield go_terms

main()