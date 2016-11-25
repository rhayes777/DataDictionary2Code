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
        self.to_manys = []

    def add_attribute(self, name, type_name):
        type_name = type_name.title()
        if type_name == "Double":
            type_name = "Float"
        if type_name == "Datetime":
            type_name = "DateTime"
        self.type_names.add(type_name)
        self.attributes.append((name, type_name))

    def add_to_many(self, name, backref, child_class):
        self.to_manys.append((name, backref, child_class))


class Maker:
    def __init__(self, filename="model.py"):
        self.filename = filename
        self.classes = []
        self.type_names = set()
        self.is_relationship = False

    def add_class(self, cls):
        self.classes.append(cls)
        self.type_names.update(cls.type_names)
        if cls.to_manys:
            self.type_names.add("ForeignKey")
            self.is_relationship = True

    def write(self):
        with open(self.filename, "w") as f:
            f.write(HEAD_TEXT)
            if self.type_names:
                f.write("\nfrom sqlalchemy import %s" % ", ".join(self.type_names))
            if self.is_relationship:
                f.write("\nfrom sqlalchemy.orm import relationship")
            for cls in self.classes:
                f.write("\n\nclass %s:" % cls.name)
                if cls.attributes:
                    for attribute in cls.attributes:
                        f.write("%s%s = Column(%s)" % (NEW_LINE_INDENT, attribute[0], attribute[1]))
                if cls.to_manys:
                    for to_many in cls.to_manys:
                        f.write("%s%s = relationship(\"%s\", backref=\"%s\")" % (
                            NEW_LINE_INDENT, to_many[0], to_many[2].name, to_many[1]))
                        # comments = db.relationship("Comment", backref="session")
                if not cls.attributes and not cls.to_manys:
                    f.write("%spass" % NEW_LINE_INDENT)
