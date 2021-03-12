import unittest
import bridges.utils as utils


class TestUtils(unittest.TestCase):
    """
    Tests of the file containg utils functions
    """

    def test_get_url(self):
        self.assertEqual('title-1', utils.get_url('title', 1))

    def test_get_url_from_title(self):
        self.assertEqual('asd--ue-v--r-', utils.get_url_from_title('asd,-ue/v.]r]'))

    def test_get_url_and_number(self):
        self.assertDictEqual({'url': 'title', 'number': 10}, utils.get_url_and_number('title-10'))

    def test_dict_subset(self):
        self.assertDictEqual({'key1': 'value1'}, utils.dict_subset({'key1': 'value1', 'key2': 'value2'}, {'key1'}))

    def test_sanitize(self):
        self.assertEqual('very', utils.sanitize('very very very very long string', max_length=4))
        self.assertEqual('first line \n second line',
            utils.sanitize('first line \n second line \n third line', max_lines=2))