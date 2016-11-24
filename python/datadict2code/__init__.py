INDENT = "    "
NEW_LINE_INDENT = "\n%s" % INDENT


class Maker:

    def __init__(self, filename="model.py"):
        self.filename = filename
        self.f = open(filename, "w")

    def add_class(self, class_name):
        self.f.write("\n\nclass %s:%spass" % (class_name, NEW_LINE_INDENT))

    def close(self):
        self.f.close()
