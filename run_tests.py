import sys
import unittest
from tests.test_main import MainPageTest, NewTestCase

if __name__ == '__main__':
    suite = unittest.TestSuite((
        unittest.makeSuite(NewTestCase),
    ))
    result = unittest.TextTestRunner().run(suite)
    sys.exit(not result.wasSuccessful())
