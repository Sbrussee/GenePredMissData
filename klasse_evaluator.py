import numpy as np
class input_training_evaluator:

    def __init__(self, true_terms):
        self.go_assignment = {}
        self.go_terms = []
        self.true_go_terms = []
        self.true_terms = true_terms

    # Functie voor het berekenen van de true terms in de dictionaire van de trainingsdata
    def set_true_terms(self):
        for terms in self.true_terms.values():
            for term in terms:
                if term not in self.true_go_terms:
                    self.true_go_terms.append(term)

    # Functie om de unieke go_termen aan te maken.
    def get_terms(self, genen, getal):
        self.go_assignment[getal] = genen
        for terms in genen:
            if terms not in self.go_terms:
                self.go_terms.append(terms)

    # Functie om een numpy array te maken voor de training input evaluator.
    def get_training(self):
        len_go_assignment = len(self.go_assignment)
        len_go_terms = len(self.go_terms)
        input_evaluator = np.zeros((len_go_assignment, len_go_terms), dtype="int")
        for gen, terms in self.go_assignment.items():
            for a in terms:
                index = self.go_terms.index(a)
                input_evaluator[gen, index] = 1
        yield input_evaluator

    # Functie om een numpy array te maken voor de test input evaluator.
    def get_test(self):
        len_go_assignment = len(self.true_terms)
        len_go_terms = len(self.true_go_terms)
        input_evaluator = np.zeros((len_go_assignment, len_go_terms), dtype="int")
        for gen, terms in self.true_terms.items():
            for a in terms:
                index = self.true_go_terms.index(a)
                input_evaluator[gen, index] = 1
        yield input_evaluator


if __name__ == "__main__":
    true_assignment = {
        0: ["go1", "go2", "go3", "go4", "go5", "go6", "go7", "go8", "go9", "go10", "go11", "go12", "go13"],
        1: ["go14", "go15", "go16", "go17", "go22", "go33", "go11", "go8", "go9", "go112", "go119", "go159", "go13"],
        2: ["go1", "go2", "go35", "go4", "go5", "go56", "go755", "go8", "go99", "go10", "go11", "go12", "go133"],
        3: ["go1", "go12", "go3", "go44", "go54", "go20", "go17", "go98", "go93", "go10", "go11", "go12", "go13"],
        4: ["go1", "go2", "go3", "go4", "go5", "go6", "go7", "go8", "go9", "go10", "go11", "go12", "go1344"]}

    # A test example dataset
    gen1 = ["go1", "go2", "go3", "go4", "go5", "go6", "go7", "go8", "go9", "go10", "go11", "go12", "go13"]
    gen2 = ["go14", "go15", "go16", "go17", "go22", "go33", "go11", "go8", "go9", "go112", "go119", "go159", "go13"]
    gen3 = ["go1", "go2", "go35", "go4", "go5", "go56", "go755", "go8", "go99", "go10", "go11", "go12", "go133"]
    gen4 = ["go1", "go12", "go3", "go44", "go54", "go20", "go17", "go98", "go93", "go10", "go11", "go12", "go13"]
    gen5 = ["go1", "go2", "go3", "go4", "go5", "go6", "go7", "go8", "go9", "go10", "go11", "go12", "go1344"]
    genen = [gen1, gen2, gen3, gen4, gen5]

    klasse = input_training_evaluator(true_assignment)
    klasse.set_true_terms()
    for getal, lijst in enumerate(genen):
        klasse.get_terms(lijst, getal)

    evaluator_training = klasse.get_training()
    evaluator_test = klasse.get_test()
    print("Test set:\n",next(evaluator_test))
    print("\n\nTraining_set:\n", next(evaluator_training))

