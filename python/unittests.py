import unittest
from datadict2code import Maker, Class
import inspect
import os
from sqlalchemy import DateTime, String, Integer, Float
import model


def get_class_double(class_name):
    classes = inspect.getmembers(model, inspect.isclass)
    ls = filter(lambda cls: cls[0] == class_name, classes)
    if ls:
        return ls[0]


def get_attribute_double(class_name, function_name):
    ls = filter(lambda att: att[0] == function_name,
                inspect.getmembers(get_class_double(class_name)[1],
                                   lambda a: not (inspect.isroutine(a))))
    if ls:
        return ls[0]


class BasicTestCase(unittest.TestCase):
    def setUp(self):
        self.maker = Maker()

    def tearDown(self):
        os.system("rm model.py")

    def test_code_creation(self):
        self.maker.add_class(Class("Test"))
        self.maker.add_class(Class("SecondClass"))
        self.maker.write()
        reload(model)
        self.assertTrue("Test" in map(lambda parts: parts[0], inspect.getmembers(model, inspect.isclass)))
        self.assertTrue("SecondClass", inspect.getmembers(model, inspect.isclass)[1][0])

    def test_attribute_creation(self):
        cls = Class("Test")
        cls.add_attribute("first_name", "string")
        cls.add_attribute("flt", "double")
        cls.add_attribute("intg", "integer")
        cls.add_attribute("dt", "datetime")
        self.maker.add_class(cls)
        self.maker.write()
        reload(model)

        self.assertTrue("Test" in map(lambda parts: parts[0], inspect.getmembers(model, inspect.isclass)))

        self.assertEqual(get_attribute_double("Test", "first_name")[0], "first_name")
        self.assertEqual(get_attribute_double("Test", "flt")[0], "flt")
        self.assertEqual(get_attribute_double("Test", "intg")[0], "intg")
        self.assertEqual(get_attribute_double("Test", "dt")[0], "dt")

        self.assertTrue(isinstance(get_attribute_double("Test", "dt")[1].type, DateTime))
        self.assertTrue(isinstance(get_attribute_double("Test", "flt")[1].type, Float))
        self.assertTrue(isinstance(get_attribute_double("Test", "intg")[1].type, Integer))
        self.assertTrue(isinstance(get_attribute_double("Test", "first_name")[1].type, String))

    def test_relationships(self):
        parent = Class("Parent")
        child = Class("Child")
        parent.add_to_many("children", "parent", child)

        self.maker.add_class(parent)
        self.maker.add_class(child)
        self.maker.write()
        reload(model)

        print(inspect.getmembers(model, inspect.isclass))
        self.assertEqual(get_attribute_double("Parent", "children")[0], "children")


if __name__ == "__main__":
    unittest.main()
