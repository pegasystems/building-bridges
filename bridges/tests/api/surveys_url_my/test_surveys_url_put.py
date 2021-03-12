import json
from http import HTTPStatus
from unittest.mock import patch

from bridges.tests.api.basic_test import BasicTest, ADMIN_SECRET

SURVEYS_ENDPOINT = 'surveys/url-1'


class PutSurveysTest(BasicTest):
    def test_close_survey_normal(self):
        will_survey_be_open_after_change = False
        future = self.make_future_put_request(f'{SURVEYS_ENDPOINT}?admin_secret={ADMIN_SECRET}',
                                              dict(open=will_survey_be_open_after_change))
        # get data about survey
        self.mock_get_info_about_survey(is_open=True)
        # update survey state
        request = self.server.receives()
        request.ok({'nModified': 1})
        # get data about modified survey
        self.mock_get_info_about_survey(is_open=will_survey_be_open_after_change)
        http_response = future()
        json_result = json.loads(http_response.data.decode())
        self.assertEqual(json_result['open'], will_survey_be_open_after_change)
        self.assertEqual(http_response.status_code, HTTPStatus.CREATED)

    def test_close_survey_not_authorized(self):
        will_survey_be_open_after_change = False
        future = self.make_future_put_request(f'{SURVEYS_ENDPOINT}?admin_secret=wr0ng_s3cr3t',
                                              dict(open=will_survey_be_open_after_change))
        # get data about survey
        self.mock_get_info_about_survey(is_open=True)
        http_response = future()
        self.assertEqual(http_response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_close_non_existing_survey(self):
        will_survey_be_open_after_change = False
        future = self.make_future_put_request(f'{SURVEYS_ENDPOINT}?admin_secret={ADMIN_SECRET}',
                                              dict(open=will_survey_be_open_after_change))
        # get data about survey
        request = self.server.receives()
        request.ok(cursor={'id': 0, 'firstBatch': []})
        http_response = future()
        self.assertEqual(http_response.status_code, HTTPStatus.NOT_FOUND)

    def test_open_survey_normal(self):
        will_survey_be_open_after_change = True
        future = self.make_future_put_request(f'{SURVEYS_ENDPOINT}?admin_secret={ADMIN_SECRET}',
                                              dict(open=will_survey_be_open_after_change))
        # get data about survey
        self.mock_get_info_about_survey(is_open=False)
        # update survey state
        request = self.server.receives()
        request.ok({'nModified': 1})
        # get data about modified survey
        self.mock_get_info_about_survey(is_open=will_survey_be_open_after_change)
        http_response = future()
        json_result = json.loads(http_response.data.decode())
        self.assertEqual(json_result['open'], will_survey_be_open_after_change)
        self.assertEqual(http_response.status_code, HTTPStatus.CREATED)

    def test_open_survey_issue(self):
        will_survey_be_open_after_change = True
        future = self.make_future_put_request(f'{SURVEYS_ENDPOINT}?admin_secret={ADMIN_SECRET}',
                                              dict(open=will_survey_be_open_after_change))
        # get data about survey
        self.mock_get_info_about_survey(is_open=False)
        # update survey state
        request = self.server.receives()
        request.ok({'nModified': 0})
        http_response = future()
        self.assertEqual(http_response.status_code, HTTPStatus.NOT_FOUND)

    def test_open_survey_already_open(self):
        will_survey_be_open_after_change = True
        future = self.make_future_put_request(f'{SURVEYS_ENDPOINT}?admin_secret={ADMIN_SECRET}',
                                              dict(open=will_survey_be_open_after_change))
        # get data about survey
        self.mock_get_info_about_survey(is_open=True)
        http_response = future()
        json_result = json.loads(http_response.data.decode())
        self.assertEqual(json_result['open'], will_survey_be_open_after_change)
        self.assertEqual(http_response.status_code, HTTPStatus.CREATED)
