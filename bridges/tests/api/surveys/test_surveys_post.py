import json
from http import HTTPStatus

from mockupdb import MockupDB, go, Command
from json import dumps
import datetime
from bridges.tests.api.basic_test import BasicTest
import bridges.api.logic

SURVEYS_ENDPOINT = 'surveys/'


class PostSurveysTest(BasicTest):
    def test_normal(self):
        future = self.make_future_post_request(SURVEYS_ENDPOINT, dict(title="title", hideVotes=True))
        # get new survey number
        request = self.server.receives()
        request.ok(cursor={'id': 0, 'firstBatch': []})
        # insert new survey
        request = self.server.receives()
        request.ok()
        http_response = future()
        self.assertEqual(http_response.status_code, HTTPStatus.CREATED)
        json_result = json.loads(http_response.data.decode())
        self.assertIn('results_secret', json_result)
        self.assertIn('admin_secret', json_result)
        self.assertEqual('title-1', json_result['key'])

    def test_without_hide_votes(self):
        future = self.make_future_post_request(SURVEYS_ENDPOINT, dict(title="title"))
        # get new survey number
        request = self.server.receives()
        request.ok(cursor={'id': 0, 'firstBatch': []})
        # insert new survey
        request = self.server.receives()
        request.ok()
        http_response = future()
        self.assertEqual(http_response.status_code, HTTPStatus.CREATED)

    def test_bad_request(self):
        future = self.make_future_post_request(SURVEYS_ENDPOINT, dict(this_is_bad_title_key="title"))
        http_response = future()
        self.assertEqual(http_response.status_code, HTTPStatus.BAD_REQUEST)

    def test_serverIssue(self):
        def broken_create_survey(title, hide_votes, description, author):
            raise ArithmeticError

        temp = bridges.api.logic.create_survey
        bridges.api.logic.create_survey = broken_create_survey

        future = self.make_future_post_request(SURVEYS_ENDPOINT, dict(title="title"))
        http_response = future()

        bridges.api.logic.create_survey = temp
        self.assertEqual(
            http_response.status_code,
            HTTPStatus.INTERNAL_SERVER_ERROR)
