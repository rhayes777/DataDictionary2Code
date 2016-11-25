import writer
import csv


class Parser:
    def __init__(self, filename):
        self.f = open(filename, 'rb')
        self.reader = csv.reader(self.f)

    def class_list(self):
        return map(lambda row: writer.Class(row[0], description=row[1]),self.reader)

    def close(self):
        self.f.close()

