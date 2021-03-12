import json
from http import HTTPStatus

from mockupdb import MockupDB, go, Command, OpReply
from json import dumps
import datetime
from bridges.tests.api.basic_test import BasicTest
import bridges.api.logic

QUESTIONS_ENDPOINT = 'surveys/test-1/questions/'


class PutVoteTest(BasicTest):
    def test_normal(self):
        future = self.make_future_put_request(
            f'{QUESTIONS_ENDPOINT}{str(self.example_ids[1])}/vote?type=up')
        # get data about survey
        self.mock_get_info_about_survey()
        # remove user vote
        request = self.server.receives()
        request.ok({'nModified': 1})
        # add new user vote
        request = self.server.receives()
        request.ok({'nModified': 1})
        http_response = future()
        self.assertEqual(http_response.status_code, HTTPStatus.CREATED)

    def test_not_add_vote_in_closed_survey(self):
        future = self.make_future_put_request(
            f'{QUESTIONS_ENDPOINT}{str(self.example_ids[1])}/vote?type=up')
        # get data about survey
        self.mock_get_info_about_survey(is_open=False)
        http_response = future()
        self.assertEqual(http_response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

    def test_bad_request_value(self):
        future = self.make_future_put_request(
            f'{QUESTIONS_ENDPOINT}{str(self.example_ids[1])}/vote?type=bad_value')
        http_response = future()
        self.assertEqual(http_response.status_code, HTTPStatus.BAD_REQUEST)

    def test_bad_request_key(self):
        future = self.make_future_put_request(
            f'{QUESTIONS_ENDPOINT}{str(self.example_ids[1])}/vote?bad_type=up')
        http_response = future()
        self.assertEqual(http_response.status_code, HTTPStatus.BAD_REQUEST)

    def test_notFound(self):
        future = self.make_future_put_request(
            f'{QUESTIONS_ENDPOINT}{str(self.example_ids[1])}/vote?type=up')
        # get data about survey
        self.mock_get_info_about_survey()
        # remove user vote
        request = self.server.receives()
        request.ok({'nModified': 0})
        # add new user vote
        request = self.server.receives()
        request.ok({'nModified': 0})
        http_response = future()
        self.assertEqual(http_response.status_code, HTTPStatus.CREATED)
