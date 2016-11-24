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
        self.assertEqual("Test", inspect.getmembers(model, inspect.isclass)[2][0])
        self.assertEqual("SecondClass", inspect.getmembers(model, inspect.isclass)[1][0])

    # def test_attribute_creation(self):
    #     self.maker.add_class(class_name="FunctionClass", attributes={"first_name": "String"})


if __name__ == "__main__":
    unittest.main()
