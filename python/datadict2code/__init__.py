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


class Maker:
    def __init__(self, filename="model.py"):
        self.filename = filename
        self.f = open(filename, "w")
        self.f.write(HEAD_TEXT)

    def add_class(self, class_name):
        self.f.write("\n\nclass %s:%spass" % (class_name, NEW_LINE_INDENT))

    def close(self):
        self.f.close()
