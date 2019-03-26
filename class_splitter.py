import random

class Splitter:
    def __init__(self, percentage, count):
        self.percentage = percentage
        self.count = count

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
        test_split = 100 - test_data
        with open("mgi.gaf", "r") as source:
            lines = [line for line in source]
        random_choice = random.sample(lines, test_split)
        with open("test_file.txt", "w") as new:
            new.write("\n".join(random_choice))
        print("Done")

    




