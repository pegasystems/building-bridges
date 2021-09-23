from http import HTTPStatus

from bridges.tests.api.basic_test import BasicTest
from bridges.tests.api.basic_test import BasicTest, ADMIN_SECRET

QUESTION_ENDPOINT = 'surveys/test-1/questions/'


class HideQuestionTest(BasicTest):
    def test_normal(self):
        hidden = True
        future = self.make_future_put_request(f'{QUESTION_ENDPOINT}{str(self.example_ids[1])}?admin_secret={ADMIN_SECRET}',
                                              {'hidden': hidden})
        # get data about survey
        self.mock_get_info_about_survey()
        request = self.server.receives()
        request.ok({'nModified': 1})
        http_response = future()
        self.assertEqual(http_response.status_code, HTTPStatus.OK)


    def test_hide_question_not_authorized(self):
        hidden = True
        future = self.make_future_put_request(f'{QUESTION_ENDPOINT}{str(self.example_ids[1])}?admin_secret=BAD',
                                              {'hidden': hidden})
        # get data about survey
        self.mock_get_info_about_survey()
        http_response = future()
        self.assertEqual(http_response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_hide_non_existing_question(self):
        hidden = True
        future = self.make_future_put_request(f'{QUESTION_ENDPOINT}{str(self.example_ids[1])}?admin_secret={ADMIN_SECRET}',
                                              {'hidden': hidden})
        request = self.server.receives()
        request.ok(cursor={'id': 0, 'firstBatch': []})
        http_response = future()
        self.assertEqual(http_response.status_code, HTTPStatus.NOT_FOUND)