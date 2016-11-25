import re

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


def lower_camel_case(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


class Class:
    def __init__(self, name):
        self.name = name
        self.attributes = []
        self.type_names = set()
        self.relationships = []
        self.tablename = lower_camel_case(name)

    def add_attribute(self, name, type_name):
        type_name = type_name.title()
        if type_name == "Double":
            type_name = "Float"
        if type_name == "Datetime":
            type_name = "DateTime"
        self.type_names.add(type_name)
        self.attributes.append((name, type_name))

    def write(self, f):
        f.write("\n\nclass %s(Base):" % self.name)
        f.write("%s__tablename__ = '%s'" % (NEW_LINE_INDENT, self.tablename))
        f.write("%sid = Column(Integer, primary_key=True)" % NEW_LINE_INDENT)

        for attribute in self.attributes:
            f.write("%s%s = Column(%s)" % (NEW_LINE_INDENT, attribute[0], attribute[1]))

        for relationship in self.relationships:
            relationship.write_for_class(self, f)


class Relationship:
    def __init__(self, first_class, second_class, first_attribute, second_attribute, ondelete="SET NULL"):
        self.first_class = first_class
        self.second_class = second_class
        self.first_attribute = first_attribute
        self.second_attribute = second_attribute
        self.ondelete = ondelete
        first_class.relationships.append(self)
        second_class.relationships.append(self)

    def write_foreign_key(self, attribute, cls, f):
        f.write("%s%s_id = Column(Integer, ForeignKey(\"%s.id\", ondelete=\"%s\"))" % (NEW_LINE_INDENT,
                                                                                       attribute,
                                                                                       cls.tablename,
                                                                                       self.ondelete))


class OneToMany(Relationship):
    def write_for_class(self, cls, f):
        if cls == self.first_class:
            f.write("%s%s = relationship(\"%s\", backref=\"%s\")" % (
                NEW_LINE_INDENT, self.first_attribute, self.second_class.name,
                self.second_attribute))
        elif cls == self.second_class:
            self.write_foreign_key(self.second_attribute, self.second_class, f)
        else:
            raise AssertionError("Class does not belong to relationship")


class OneToOne(Relationship):
    def write_for_class(self, cls, f):
        if cls == self.first_class:
            f.write("%s%s = relationship(\"%s\", uselist=False, back_populates=\"%s\")" % (
                NEW_LINE_INDENT, self.first_attribute, self.second_class.name,
                self.second_attribute))
        elif cls == self.second_class:
            f.write("%s%s = relationship(\"%s\", back_populates=\"%s\")" % (
                NEW_LINE_INDENT, self.second_attribute, self.first_class.name,
                self.first_attribute))
            self.write_foreign_key(self.second_attribute, self.second_class, f)
        else:
            raise AssertionError("Class does not belong to relationship")


class ManyToMany(Relationship):
    def write_for_class(self, cls, f):
        if cls == self.first_class:
            f.write("%s%s = relationship(\"%s\", secondary=%s, back_populates=\"%s\")" % (
                NEW_LINE_INDENT, self.first_attribute, self.second_class.name, self.association_table_name(),
                self.second_attribute))
        elif cls == self.second_class:
            f.write("%s%s = relationship(\"%s\", secondary=%s, back_populates=\"%s\")" % (
                NEW_LINE_INDENT, self.second_attribute, self.first_class.name, self.association_table_name(),
                self.first_attribute))
        else:
            raise AssertionError("Class does not belong to relationship")

    def write_association_table(self, f):
        f.write(
            """{0}{1} = Table('{1}', Base.metadata,
            Column('{2}_id', Integer, ForeignKey('{2}.id')),
            Column('{3}_id', Integer, ForeignKey('{3}.id')))""".format('\n', self.association_table_name(),
                                                                       self.first_class.tablename,
                                                                       self.second_class.tablename))

    def association_table_name(self):
        return "%s_%s_association" % (self.first_class.tablename,
                                      self.second_class.tablename)


class Writer:
    def __init__(self, filename="model"):
        self.filename = filename
        self.classes = []
        self.type_names = set()
        self.type_names.add("Integer")

    def add_class(self, cls):
        self.classes.append(cls)
        self.type_names.update(cls.type_names)

    def is_relationship(self):
        for cls in self.classes:
            if cls.relationships:
                return True

    def get_relationships(self):
        relationships = set()
        for cls in self.classes:
            relationships.update(cls.relationships)
        return relationships

    def write(self):
        with open("%s.py" % self.filename, "w") as f:
            f.write(HEAD_TEXT)
            many_to_manys = filter(lambda relationship: isinstance(relationship, ManyToMany), self.get_relationships())
            if many_to_manys:
                self.type_names.add("Table")
            if self.type_names:
                f.write("\nfrom sqlalchemy import %s" % ", ".join(self.type_names))
            if self.is_relationship():
                f.write("\nfrom sqlalchemy import ForeignKey")
                f.write("\nfrom sqlalchemy.orm import relationship")

            for many_to_many in many_to_manys:
                many_to_many.write_association_table(f)

            for cls in self.classes:
                cls.write(f)
