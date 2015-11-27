import sys
import unittest
from tests.test_main import MainPageTest, NewsBlockTest, PersonalInfoTestCase, TopBarTest

if __name__ == '__main__':
    suite = unittest.TestSuite((
        unittest.makeSuite(MainPageTest),
        unittest.makeSuite(TopBarTest),
        unittest.makeSuite(PersonalInfoTestCase),
        unittest.makeSuite(NewsBlockTest)
    ))
    result = unittest.TextTestRunner().run(suite)
    sys.exit(not result.wasSuccessful())
