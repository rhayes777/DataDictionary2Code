import unittest
import datadict2code
import classes
import inspect


class BasicTestCase(unittest.TestCase):
    def test_code_creation(self):
        datadict2code.create_class(name="Test")
        reload(classes)
        self.assertTrue("Test" == inspect.getmembers(classes, inspect.isclass)[0][0])


if __name__ == "__main__":
    unittest.main()
