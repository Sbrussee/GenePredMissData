import random

class Splitter:
    def __init__(self, percentage, count, input_file, output_file):
        self.percentage = percentage
        self.count = count
        self.input_file = input_file
        self.output_file = output_file

    def set_percentage(self, percentage):
        self.percentage = percentage

    def get_percentage(self):
        return self.percentage

    def set_count(self, count):
        self.count = count

    def get_count(self):
        return self.count

    def splitter(self):
        """
        Depending on the percentage and the amount of lines in the file
        it will split the data and saves the test data into a seperate file.
        """
        self.percentage
        self.count
        test_data = self.count * self.percentage // 100
        lines = [line for line in self.input_file]
        random_choice = random.sample(lines, test_data)
        with open(self.output_file, "w") as new:
            new.write("".join(random_choice))

    




