import unittest

# Discover and load all test cases in the tests folder
def run_tests():
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir="tests", pattern="test_*.py")
    runner = unittest.TextTestRunner()
    runner.run(suite)
