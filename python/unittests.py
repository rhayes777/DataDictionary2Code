import unittest
import datadict2code
import inspect
import os


class BasicTestCase(unittest.TestCase):
    def setUp(self):
        self.maker = datadict2code.Maker()

    def tearDown(self):
        os.system("rm model.py")

    def test_code_creation(self):
        self.maker.add_class(class_name="Test")
        self.maker.close()
        import model
        self.assertTrue("Test" == inspect.getmembers(model, inspect.isclass)[0][0])


if __name__ == "__main__":
    unittest.main()
