from http import HTTPStatus

from bridges.tests.api.basic_test import BasicTest
from bridges.tests.api.basic_test import BasicTest, ADMIN_SECRET

QUESTION_ENDPOINT = 'surveys/test-1/questions/'
SAMPLE_REPLY = 'sample reply'

class ReplyToQuestionTest(BasicTest):
    def test_normal(self):
        future = self.make_future_put_request(f'{QUESTION_ENDPOINT}{str(self.example_ids[1])}/reply?admin_secret={ADMIN_SECRET}',
                                              {'content': SAMPLE_REPLY})
        # get data about survey
        self.mock_get_info_about_survey()
        request = self.server.receives()
        request.ok({'nModified': 1})
        http_response = future()
        self.assertEqual(http_response.status_code, HTTPStatus.CREATED)


    def test_normal_not_authorized(self):
        future = self.make_future_put_request(f'{QUESTION_ENDPOINT}{str(self.example_ids[1])}/reply?admin_secret=BAD',
                                              {'content': SAMPLE_REPLY})
        # get data about survey
        self.mock_get_info_about_survey()
        http_response = future()
        self.assertEqual(http_response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_reply_non_existing_question(self):
        future = self.make_future_put_request(f'{QUESTION_ENDPOINT}{str(self.example_ids[1])}/reply?admin_secret={ADMIN_SECRET}',
                                              {'content': SAMPLE_REPLY})
        request = self.server.receives()
        request.ok(cursor={'id': 0, 'firstBatch': []})
        http_response = future()
        self.assertEqual(http_response.status_code, HTTPStatus.NOT_FOUND)