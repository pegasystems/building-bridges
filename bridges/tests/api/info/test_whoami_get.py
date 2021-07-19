import json
from http import HTTPStatus
from unittest.mock import patch

from bridges.tests.api.basic_test import BasicTest

DUMMY_USER_FULL_NAME = 'John Doe'
DUMMY_USER_EMAIL = 'john.doe@company.com'


class GetWhoAmITest(BasicTest):
    """
    Class to test whoami endpoint.
    """

    @patch('bridges.api.endpoints.info.get_user_name_and_email_from_session',
           return_value={'userFullName': DUMMY_USER_FULL_NAME, 'userEmail': DUMMY_USER_EMAIL})
    def test_empty(self, _):
        future = self.make_future_get_request("info/whoami")
        http_response = future()
        self.assertEqual(http_response.status_code, HTTPStatus.OK)
        data = json.loads(http_response.get_data(as_text=True))
        self.assertEquals(DUMMY_USER_FULL_NAME, data['userFullName'])
        self.assertEquals(DUMMY_USER_EMAIL, data['userEmail'])
