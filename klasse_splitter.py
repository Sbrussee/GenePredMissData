import random

class Splitter:
    def __init__(self, percentage, line_count, read_file, write_file):
        self.percentage = percentage
        self.line_count = line_count
        self.read_file = read_file
        self.write_file = write_file

    def set_percentage(self, percentage):
        self.percentage = percentage

    def get_percentage(self):
        return self.percentage

    def set_count(self, line_count):
        self.line_count = line_count

    def get_count(self):
        return self.line_count

    def splitter(self):
        """
        Depending on the percentage and the amount of lines in the file
        it will split the data and saves the test data into a seperate file.
        """
        test_data = self.line_count * self.percentage // 100
        with open(self.read_file, "r") as source:
            lines = [line for line in source]
        source.close()
        random_choice = random.sample(lines, test_data)
        with open(self.write_file, "w") as new:
            new.write("".join(random_choice))
        new.close()

    




