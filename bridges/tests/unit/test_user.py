import unittest
import bridges.utils as utils
from bridges.database.objects.user import User


class TestUser(unittest.TestCase):
    """
    Tests of the user class
    """

    def test_equal_basedOnUserId(self):
        first = User('host1', 'cookie1', 'user_id')
        second = User('host2', 'cookie2', 'user_id')
        self.assertEqual(first, second)

    def test_equal_basedOnCookie(self):
        first = User('host1', 'cookie', None)
        second = User('host2', 'cookie', None)
        self.assertEqual(first, second)

    def test_equal_basedOnHost(self):
        first = User('host', 'cookie1', None)
        second = User('host', 'cookie2', None)
        self.assertEqual(first, second)

    def test_notEqualBasedOnHostAndCookie(self):
        first = User('host1', 'cookie1', None)
        second = User('host2', 'cookie2', None)
        self.assertNotEqual(first, second)

    def test_notEqualBasedOnUserIdHostAndCookie(self):
        first = User('host', 'cookie', 'user_id1')
        second = User('host', 'cookie', 'user_id2')
        self.assertNotEqual(first, second)

    def test_equalBasedOnUserIdHostAndCookieIdOneNone(self):
        first = User('host', 'cookie', 'user_id1')
        second = User('host', 'cookie', None)
        self.assertEqual(first, second)