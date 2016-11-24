import unittest
from datadict2code import Maker, Class
import inspect
import os


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
        self.maker.add_class(cls)
        self.maker.write()
        import model

        self.assertTrue("Test" in map(lambda parts: parts[0], inspect.getmembers(model, inspect.isclass)))
        classes = inspect.getmembers(model, inspect.isclass)
        att = filter(lambda att: att[0] == "first_name",
                     inspect.getmembers(filter(lambda cls: cls[0] == "Test", classes)[0][1],
                                        lambda a: not (inspect.isroutine(a))))[0]
        self.assertEqual(att[0], "first_name")
        # self.assertTrue("first_name" in
        #                 map(lambda parts: parts[0], inspect.getmembers(inspect.getmembers(model, inspect.isclass)[1],
        #                                                                lambda a: not (inspect.isroutine(a)))))


if __name__ == "__main__":
    unittest.main()
