import unittest
import datadict2code
import inspect


class BasicTestCase(unittest.TestCase):
    def test_code_creation(self):
        maker = datadict2code.Maker()
        maker.add_class(class_name="Test")
        maker.close()
        import model
        self.assertTrue("Test" == inspect.getmembers(model, inspect.isclass)[0][0])


if __name__ == "__main__":
    unittest.main()
