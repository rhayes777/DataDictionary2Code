import writer
import csv


class Parser:
    def __init__(self, filename):
        self.f = open(filename, 'rb')
        self.reader = csv.reader(self.f)
        self.classes = map(lambda row: writer.Class(row[0], description=row[1]), self.reader)

    def add_attributes(self):
        pass
        # for n in range(0, len(classes)):
        #     self.add_attributes
        # return classes

    def close(self):
        self.f.close()
