import sys
sys.path.append('../src')
import unittest
from helper_functions import *

class testRegisterValidation(unittest.TestCase):
    def test_password(self):
        self.assertFalse(check_password_rules("password1"))
        self.assertFalse(check_password_rules("PASSWORD1"))
        self.assertFalse(check_password_rules("Password"))
        self.assertFalse(check_password_rules("Pass1"))
        self.assertFalse(check_password_rules("Abcdefghi123456789"))
        self.assertTrue(check_password_rules("Password1234"))
    def test_username(self):
        self.assertFalse(check_valid_username("Usuario1234567890"))
        self.assertTrue(check_valid_username("Usuario123456789"))
    def test_image(self):
        self.assertFalse(check_valid_imagetype("executable"))
        self.assertTrue(check_valid_imagetype("image/jpeg"))


if __name__ == '__main__':
    unittest.main()