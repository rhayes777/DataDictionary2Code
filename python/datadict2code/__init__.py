import writer
import csv


class Parser:
    def __init__(self, filename):
        self.f = open(filename, 'rb')
        self.reader = csv.reader(self.f)

    def class_list(self):
        class_list = []
        for row in self.reader:
            class_list.append(writer.Class(row[0], description=row[1]))
        return class_list

