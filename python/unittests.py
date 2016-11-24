import unittest
from datadict2code import Maker, Class
import inspect
import os


def get_class_double(module, class_name):
    classes = inspect.getmembers(module, inspect.isclass)
    return filter(lambda cls: cls[0] == class_name, classes)[0]


class BasicTestCase(unittest.TestCase):
    def setUp(self):
        self.maker = Maker()

    def tearDown(self):
        os.system("rm model.py")

    def test_code_creation(self):
        self.maker.add_class(Class("Test"))
        self.maker.add_class(Class("SecondClass"))
        self.maker.write()
        import model
        self.assertTrue("Test" in map(lambda parts: parts[0], inspect.getmembers(model, inspect.isclass)))
        self.assertTrue("SecondClass", inspect.getmembers(model, inspect.isclass)[1][0])

    def test_attribute_creation(self):
        cls = Class("Test")
        cls.add_attribute("first_name", "string")
        # cls.add_attribute("flt", "double")
        # cls.add_attribute("intg", "integer")
        self.maker.add_class(cls)
        self.maker.write()
        import model

        self.assertTrue("Test" in map(lambda parts: parts[0], inspect.getmembers(model, inspect.isclass)))
        
        att = filter(lambda att: att[0] == "first_name",
                     inspect.getmembers(get_class_double(model, "Test")[1],
                                        lambda a: not (inspect.isroutine(a))))[0]
        self.assertEqual(att[0], "first_name")


if __name__ == "__main__":
    unittest.main()
