import unittest
import bridges.utils as utils
from bridges.database.objects.user import User


class TestUser(unittest.TestCase):
    """
    Tests of the user class
    """

    def test_equal_basedOnUserId(self):
        first = User('host1', 'cookie1', 'user_id', None, None)
        second = User('host2', 'cookie2', 'user_id', None, None)
        self.assertEqual(first, second)

    def test_equal_basedOnCookie(self):
        first = User('host1', 'cookie', None, None, None)
        second = User('host2', 'cookie', None, None, None)
        self.assertEqual(first, second)

    def test_equal_basedOnHost(self):
        first = User('host', 'cookie1', None, None, None)
        second = User('host', 'cookie2', None, None, None)
        self.assertNotEqual(first, second)

    def test_notEqualBasedOnHostAndCookie(self):
        first = User('host1', 'cookie1', None, None, None)
        second = User('host2', 'cookie2', None, None, None)
        self.assertNotEqual(first, second)

    def test_notEqualBasedOnUserIdHostAndCookie(self):
        first = User('host', 'cookie', 'user_id1', None, None)
        second = User('host', 'cookie', 'user_id2', None, None)
        self.assertNotEqual(first, second)

    def test_equalBasedOnUserIdHostAndCookieIdOneNone(self):
        first = User('host', 'cookie', 'user_id1', None, None)
        second = User('host', 'cookie', None, None, None)
        self.assertEqual(first, second)
