import unittest
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


class BasicTestCase(unittest.TestCase):
    def tearDown(self):
        os.system("rm model*")

    def assertClassExists(self, module, class_name):
        self.assertIsNotNone(get_class_double(module, class_name))

    def assertAttributeExists(self, module, class_name, attribute_name):
        self.assertIsNotNone(get_attribute_double(module, class_name, attribute_name))

    def test_code_creation(self):
        maker = Maker("model_code_creation")
        maker.add_class(Class("Test"))
        maker.add_class(Class("SecondClass"))
        maker.write()
        import model_code_creation
        self.assertTrue("Test" in map(lambda parts: parts[0], inspect.getmembers(model_code_creation, inspect.isclass)))
        self.assertIsNotNone(get_class_double(model_code_creation, "SecondClass"))
        self.assertEqual("second_class", get_class_double(model_code_creation, "SecondClass")[1].__tablename__)

    def test_attribute_creation(self):
        maker = Maker("model_attribute_creation")
        cls = Class("Test")
        cls.add_attribute("first_name", "string")
        cls.add_attribute("flt", "double")
        cls.add_attribute("intg", "integer")
        cls.add_attribute("dt", "datetime")
        maker.add_class(cls)
        maker.write()
        import model_attribute_creation

        self.assertTrue(
            "Test" in map(lambda parts: parts[0], inspect.getmembers(model_attribute_creation, inspect.isclass)))

        self.assertEqual(get_attribute_double(model_attribute_creation, "Test", "first_name")[0], "first_name")
        self.assertEqual(get_attribute_double(model_attribute_creation, "Test", "flt")[0], "flt")
        self.assertEqual(get_attribute_double(model_attribute_creation, "Test", "intg")[0], "intg")
        self.assertEqual(get_attribute_double(model_attribute_creation, "Test", "dt")[0], "dt")

        self.assertTrue(isinstance(get_attribute_double(model_attribute_creation, "Test", "dt")[1].type, DateTime))
        self.assertTrue(isinstance(get_attribute_double(model_attribute_creation, "Test", "flt")[1].type, Float))
        self.assertTrue(isinstance(get_attribute_double(model_attribute_creation, "Test", "intg")[1].type, Integer))
        self.assertTrue(
            isinstance(get_attribute_double(model_attribute_creation, "Test", "first_name")[1].type, String))

    def test_one_to_many_relationship(self):
        maker = Maker("model_one_to_many_relationships")
        parent = Class("Parent")
        child = Class("Child")
        OneToMany(parent, child, "children", "parent")

        maker.add_class(parent)
        maker.add_class(child)
        maker.write()
        import model_one_to_many_relationships

        self.assertEqual(get_attribute_double(model_one_to_many_relationships, "Parent", "children")[0], "children")
        self.assertEqual(get_attribute_double(model_one_to_many_relationships, "Child", "parent_id")[0], "parent_id")

    def test_one_to_one_relationship(self):
        maker = Maker("model_one_to_one_relationship")
        first = Class("First")
        second = Class("Second")
        OneToOne(first, second, "second", "first")

        maker.add_class(first)
        maker.add_class(second)

        maker.write()

        import model_one_to_one_relationship

        self.assertAttributeExists(model_one_to_one_relationship, "First", "second")
        self.assertAttributeExists(model_one_to_one_relationship, "Second", "first")


if __name__ == "__main__":
    unittest.main()
