import unittest
import bridges.utils as utils
from bridges.database.objects.user import User


class TestUser(unittest.TestCase):
    """
    Tests of the user class
    """

    def test_equal_basedOnUserId(self):
        first = User('cookie1', 'user_id', None, None)
        second = User('cookie2', 'user_id', None, None)
        self.assertEqual(first, second)

    def test_equal_basedOnCookie(self):
        first = User('cookie', None, None, None)
        second = User('cookie', None, None, None)
        self.assertEqual(first, second)

    def test_notEqualBasedOnUserIdAndCookie(self):
        first = User('cookie', 'user_id1', None, None)
        second = User('cookie', 'user_id2', None, None)
        self.assertNotEqual(first, second)

    def test_equalBasedOnUserIdAndCookieIdOneNone(self):
        first = User('cookie', 'user_id1', None, None)
        second = User('cookie', None, None, None)
        self.assertEqual(first, second)
