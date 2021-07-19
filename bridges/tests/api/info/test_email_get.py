import json
from http import HTTPStatus

from bridges.tests.api.basic_test import BasicTest


class GetEmailTest(BasicTest):
    """
    Class to test email endpoint.
    """

    def test_empty(self):
        future = self.make_future_get_request("info/email")
        http_response = future()
        self.assertEqual(http_response.status_code, HTTPStatus.OK)
        data = http_response.get_data(as_text=True)
        self.assertIn('email@example.com', data)
