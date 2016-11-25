import unittest
from datadict2code.writer import *
from datadict2code import *
import inspect
import os
from sqlalchemy import DateTime, String, Integer, Float


def get_class_double(module, class_name):
    classes = inspect.getmembers(module, inspect.isclass)
    ls = filter(lambda cls: cls[0] == class_name, classes)
    if ls:
        return ls[0]


def get_attribute_double(module, class_name, function_name):
    ls = filter(lambda att: att[0] == function_name,
                inspect.getmembers(get_class_double(module, class_name)[1],
                                   lambda a: not (inspect.isroutine(a))))
    if ls:
        return ls[0]


class WriterTestCase(unittest.TestCase):
    def tearDown(self):
        os.system("rm model*")

    def assertClassExists(self, module, class_name):
        self.assertIsNotNone(get_class_double(module, class_name))

    def assertAttributeExists(self, module, class_name, attribute_name):
        self.assertIsNotNone(get_attribute_double(module, class_name, attribute_name))

    def test_code_creation(self):
        writer = Writer("model_code_creation")
        writer.add_class(Class("Test"))
        writer.add_class(Class("SecondClass"))
        writer.write()
        import model_code_creation
        self.assertTrue("Test" in map(lambda parts: parts[0], inspect.getmembers(model_code_creation, inspect.isclass)))
        self.assertIsNotNone(get_class_double(model_code_creation, "SecondClass"))
        self.assertEqual("second_class", get_class_double(model_code_creation, "SecondClass")[1].__tablename__)

    def test_attribute_creation(self):
        writer = Writer("model_attribute_creation")
        cls = Class("Test")
        cls.add_attribute("first_name", "string")
        cls.add_attribute("flt", "double")
        cls.add_attribute("intg", "integer")
        cls.add_attribute("dt", "datetime")
        writer.add_class(cls)
        writer.write()
        import model_attribute_creation

        self.assertTrue(
            "Test" in map(lambda parts: parts[0], inspect.getmembers(model_attribute_creation, inspect.isclass)))

        self.assertAttributeExists(model_attribute_creation, "Test", "first_name")
        self.assertAttributeExists(model_attribute_creation, "Test", "flt")
        self.assertAttributeExists(model_attribute_creation, "Test", "intg")
        self.assertAttributeExists(model_attribute_creation, "Test", "dt")

        self.assertTrue(isinstance(get_attribute_double(model_attribute_creation, "Test", "dt")[1].type, DateTime))
        self.assertTrue(isinstance(get_attribute_double(model_attribute_creation, "Test", "flt")[1].type, Float))
        self.assertTrue(isinstance(get_attribute_double(model_attribute_creation, "Test", "intg")[1].type, Integer))
        self.assertTrue(
            isinstance(get_attribute_double(model_attribute_creation, "Test", "first_name")[1].type, String))

    def test_one_to_many_relationship(self):
        writer = Writer("model_one_to_many_relationships")
        parent = Class("Parent")
        child = Class("Child")
        OneToMany(parent, child, "children", "parent")

        writer.add_class(parent)
        writer.add_class(child)
        writer.write()
        import model_one_to_many_relationships

        self.assertAttributeExists(model_one_to_many_relationships, "Parent", "children")
        self.assertAttributeExists(model_one_to_many_relationships, "Child", "parent_id")

    def test_one_to_one_relationship(self):
        writer = Writer("model_one_to_one_relationship")
        first = Class("First")
        second = Class("Second")
        OneToOne(first, second, "second", "first")

        writer.add_class(first)
        writer.add_class(second)

        writer.write()
        import model_one_to_one_relationship

        self.assertAttributeExists(model_one_to_one_relationship, "First", "second")
        self.assertAttributeExists(model_one_to_one_relationship, "Second", "first")

    def test_many_to_many_relationship(self):
        writer = Writer("model_many_to_many_relationship")
        first = Class("First")
        second = Class("Second")
        ManyToMany(first, second, "second_list", "first_list")

        writer.add_class(first)
        writer.add_class(second)

        writer.write()
        import model_many_to_many_relationship

        self.assertAttributeExists(model_many_to_many_relationship, "First", "second_list")
        self.assertAttributeExists(model_many_to_many_relationship, "Second", "first_list")

    def test_inheritance(self):
        writer = Writer("model_inheritance")
        parent = Class("Parent")
        child = Class("Child", parent=parent)

        writer.add_class(parent)
        writer.add_class(child)

        writer.write()
        import model_inheritance

        self.assertTrue(issubclass(model_inheritance.Child, model_inheritance.Parent))


class ParserTestCase(unittest.TestCase):
    def test_opening_parser(self):
        parser = Parser("example.csv")
        self.assertEqual(len(parser.class_list()), 52)


if __name__ == "__main__":
    unittest.main()
