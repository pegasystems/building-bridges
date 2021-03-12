import json
from http import HTTPStatus

from mockupdb import MockupDB, go, Command, OpReply
from json import dumps
import datetime
from bridges.tests.api.basic_test import BasicTest

QUESTIONS_ENDPOINT = 'surveys/test-1/questions/'


class DeleteVoteTest(BasicTest):
    def test_normal(self):
        future = self.make_future_delete_request(f'{QUESTIONS_ENDPOINT}{str(self.example_ids[1])}/vote')
        # get data about survey
        self.mock_get_info_about_survey()
        # remove user vote
        request = self.server.receives()
        request.ok({'nModified': 1})
        http_response = future()
        self.assertEqual(http_response.status_code, HTTPStatus.NO_CONTENT)

    def test_not_delete_vote_in_closed_survey(self):
        future = self.make_future_delete_request(f'{QUESTIONS_ENDPOINT}{str(self.example_ids[1])}/vote')
        # get data about survey
        self.mock_get_info_about_survey(is_open=False)
        http_response = future()
        self.assertEqual(http_response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

    def test_notFound(self):
        future = self.make_future_delete_request(f'{QUESTIONS_ENDPOINT}{str(self.example_ids[1])}/vote')
        # get data about survey
        self.mock_get_info_about_survey()
        # remove user vote
        request = self.server.receives()
        request.ok({'nModified': 0})
        http_response = future()
        self.assertEqual(http_response.status_code, HTTPStatus.NOT_FOUND)
