import json
from http import HTTPStatus

from mockupdb import MockupDB, go, Command, OpReply
from json import dumps
import datetime
from bridges.tests.api.basic_test import BasicTest
import bridges.api.logic

QUESTION_ENDPOINT = 'surveys/test-1/questions/'


class DeleteQuestionTest(BasicTest):
    def test_normal(self):
        future = self.make_future_delete_request(f'{QUESTION_ENDPOINT}{str(self.example_ids[1])}')
        # get data about survey
        self.mock_get_info_about_survey()
        # find question
        request = self.server.receives()
        timestamp = datetime.datetime.now()
        request.ok(cursor={'id': 0, 'firstBatch': [{
            "_id": self.example_ids[0],
            "title": "exampleTitle",
            "description": "example_description",
            "number": 1,
            'author': {
                "host": "localhost",
                "cookie": "cookie"
            },
            "url": "example-url",
            "date": timestamp,
            "questions": [
                {
                    "content": "example-content",
                    'author': {
                        "host": "localhost",
                        "cookie": "cookie"
                    },
                    "date": timestamp,
                    "votes": [],
                    "_id": self.example_ids[1]
                }
            ]}]})
        request = self.server.receives()
        request.ok({'nModified': 1})
        http_response = future()
        self.assertEqual(http_response.status_code, HTTPStatus.NO_CONTENT)

    def test_not_delete_comment_in_disabled_survey(self):
        future = self.make_future_delete_request(f'{QUESTION_ENDPOINT}{str(self.example_ids[1])}')
        # get data about survey
        self.mock_get_info_about_survey(asking_questions_enabled=False)
        http_response = future()
        self.assertEqual(http_response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

    def test_notFound(self):
        future = self.make_future_delete_request(f'{QUESTION_ENDPOINT}{str(self.example_ids[0])}')
        # get data about survey
        self.mock_get_info_about_survey()
        # find question
        request = self.server.receives()
        request.ok(cursor={'id': 0, 'firstBatch': []})
        http_response = future()
        self.assertEqual(http_response.status_code, HTTPStatus.NOT_FOUND)

    def test_notAuthorized(self):
        self.client.set_cookie('surveys/url-1', 'CLIENT_ID', 'not-my-cookie')
        future = self.make_future_delete_request(f'{QUESTION_ENDPOINT}{str(self.example_ids[1])}')
        # get data about survey
        self.mock_get_info_about_survey()
        # find question
        request = self.server.receives()
        timestamp = datetime.datetime.now()
        request.ok(cursor={'id': 0, 'firstBatch': [{
            "_id": self.example_ids[0],
            "title": "exampleTitle",
            "description": "example_description",
            "number": 1,
            "author": "localhost",
            "url": "example-url",
            "date": timestamp,
            "questions": [
                {
                    "content": "example-content",
                    'author': {"host": "NOT-MY-IP", "cookie": "cookie"},
                    "date": timestamp,
                    "votes": [],
                    "_id": self.example_ids[1]
                }
            ]}]})
        http_response = future()
        self.assertEqual(http_response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_Forbidden(self):
        self.client.set_cookie('surveys/url-1', 'CLIENT_ID', 'cookie')
        future = self.make_future_delete_request(f'{QUESTION_ENDPOINT}{str(self.example_ids[1])}')
        # get data about survey
        self.mock_get_info_about_survey()
        # find question
        request = self.server.receives()
        timestamp = datetime.datetime.now()
        request.ok(cursor={'id': 0, 'firstBatch': [{
            "_id": self.example_ids[0],
            "title": "exampleTitle",
            "description": "example_description",
            "number": 1,
            'author': {"host": "localhost", "cookie": "cookie"},
            "url": "example-url",
            "date": timestamp,
            "questions": [
                {
                    "content": "example-content",
                    'author': {"host": "localhost", "cookie": "cookie"},
                    "date": timestamp,
                    "votes": [
                        {
                            'author': {"host": "localhost", "cookie": "cookie"},
                            "upvote": True,
                            "date": timestamp
                        }
                    ],
                    "_id": self.example_ids[1],
                }
            ]}]})
        http_response = future()
        self.assertEqual(http_response.status_code, HTTPStatus.FORBIDDEN)
