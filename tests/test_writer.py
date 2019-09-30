import unittest
from app.models import Writer

class WriterModelTest(unittest.TestCase):
    '''
    Test class to test behaviours of the [Class] class
    Args:
        unittest.TestCase : Test case class that helps create test cases
    '''

    def setUp(self):
        '''
        Set up method that will run before every Test
        '''
        self.writer = Writer(password = 'aggy')


    def test_password_setter(self):
        self.assertTrue(self.writer.pass_secure is not None)


    def test_no_access_password(self):
        with self.assertRaises(AttributeError):
            self.writer.password


    def test_password_verification(self):
        self.assertTrue(self.writer.verify_password('aggy'))