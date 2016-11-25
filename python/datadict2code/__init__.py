import writer
import csv


class Parser:
    def __init__(self, filename):
        self.f = open(filename, 'rb')
        self.reader = map(lambda item: item, csv.reader(self.f))
        self.classes = map(lambda row: writer.Class(row[0], description=row[1]), self.reader)
        self.class_map = {}
        for cls in self.classes:
            self.class_map[cls.name] = cls

    def add_attributes(self):
        for n in range(0, len(self.classes)):
            attributes = self.reader[n][2].split("\n")
            cls = self.classes[n]
            for row in attributes:
                print(row)
                parts = row.replace(" ", "").replace(")", "(").split("(")
                if len(parts) < 2:
                    continue
                if parts[1] in self.class_map:
                    pass
                else:
                    cls.add_attribute(parts[0], parts[1])

    def close(self):
        self.f.close()
