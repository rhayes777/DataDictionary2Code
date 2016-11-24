INDENT = "    "
NEW_LINE_INDENT = "\n%s" % INDENT

HEAD_TEXT = """
from sqlalchemy import create_engine, Column
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite://')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()
"""


class Class:
    def __init__(self, name):
        self.name = name
        self.attributes = []
        self.type_names = set()

    def add_attribute(self, name, type_name):
        type_name = type_name.title()
        self.type_names.add(type_name)
        self.attributes.append((name, type_name))


class Maker:
    def __init__(self, filename="model.py"):
        self.filename = filename
        self.classes = []
        self.type_names = set()

    def add_class(self, cls):
        self.classes.append(cls)
        self.type_names.update(cls.type_names)

    def write(self):
        with open(self.filename, "w") as f:
            f.write(HEAD_TEXT)
            if self.type_names:

                f.write("\nfrom sqlalchemy import %s" % ", ".join(self.type_names))
            for cls in self.classes:
                if cls.attributes:
                    f.write("\n\nclass %s:" % cls.name)
                    for attribute in cls.attributes:
                        f.write("%s%s = Column(%s)" % (NEW_LINE_INDENT, attribute[0], attribute[1]))
                else:
                    f.write("\n\nclass %s:%spass" % (cls.name, NEW_LINE_INDENT))
