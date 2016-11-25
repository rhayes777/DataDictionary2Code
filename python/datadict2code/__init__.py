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
        self.relationships = []

    def add_attribute(self, name, type_name):
        type_name = type_name.title()
        if type_name == "Double":
            type_name = "Float"
        if type_name == "Datetime":
            type_name = "DateTime"
        self.type_names.add(type_name)
        self.attributes.append((name, type_name))


class Relationship:
    def __init__(self, first_class, second_class, first_attribute, second_attribute):
        self.first_class = first_class
        self.second_class = second_class
        self.first_attribute = first_attribute
        self.second_attribute = second_attribute
        first_class.relationships.append(self)
        second_class.relationships.append(self)


class OneToMany(Relationship):
    pass


class Maker:
    def __init__(self, filename="model"):
        self.filename = filename
        self.classes = []
        self.relationships = []
        self.type_names = set()

    def add_class(self, cls):
        self.classes.append(cls)
        self.type_names.update(cls.type_names)

    def is_relationship(self):
        for cls in self.classes:
            if cls.relationships:
                return True

    def write(self):
        with open("%s.py" % self.filename, "w") as f:
            f.write(HEAD_TEXT)
            if self.type_names:
                f.write("\nfrom sqlalchemy import %s" % ", ".join(self.type_names))
            if self.is_relationship():
                f.write("\nfrom sqlalchemy import ForeignKey")
                f.write("\nfrom sqlalchemy.orm import relationship")
            for cls in self.classes:
                f.write("\n\nclass %s:" % cls.name)

                for attribute in cls.attributes:
                    f.write("%s%s = Column(%s)" % (NEW_LINE_INDENT, attribute[0], attribute[1]))

                for relationship in cls.relationships:
                    f.write("%s%s = relationship(\"%s\", backref=\"%s\")" % (
                        NEW_LINE_INDENT, relationship.first_attribute, relationship.second_class.name,
                        relationship.second_attribute))
                    # comments = db.relationship("Comment", backref="session")
                if not cls.attributes and not self.is_relationship():
                    f.write("%spass" % NEW_LINE_INDENT)
