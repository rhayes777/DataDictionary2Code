INDENT = "    "
NEW_LINE_INDENT = "\n%s" % INDENT

HEAD_TEXT = """
from sqlalchemy import create_engine
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


class Maker:
    def __init__(self, filename="model.py"):
        self.filename = filename
        self.classes = []

    def add_class(self, cls):
        self.classes.append(cls)

    def write(self):
        with open(self.filename, "w") as f:
            f.write(HEAD_TEXT)
            for cls in self.classes:
                f.write("\n\nclass %s:%spass" % (cls.name, NEW_LINE_INDENT))
