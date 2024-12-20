import unittest
from main import extract_title


class TestMain(unittest.TestCase):
    
    # successfully find h1
    def test_extract_title1(self):
        md = """
my next case
## Another test case
# this is the h1 title 
"""
        func = extract_title(md)
        result = "this is the h1 title"
        self.assertEqual(
            func,
            result,
        )
    
    # Check that the error is raised
    def test_extract_title2(self):
        md = """
my next case
## Another test case
### this is the h1 title 
"""
        result = "No H1"
        with self.assertRaises(ValueError) as context:
            extract_title(md)
        self.assertEqual(str(context.exception), result)

if __name__ == "__main__":
    unittest.main()