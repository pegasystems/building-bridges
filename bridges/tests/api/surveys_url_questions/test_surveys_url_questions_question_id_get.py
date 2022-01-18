import json
from http import HTTPStatus

from mockupdb import MockupDB, go, Command
from json import dumps
import datetime
from bridges.tests.api.basic_test import BasicTest
import bridges.api.logic

QUESTIONS_ENDPOINT = 'surveys/url-1/questions/'

class GetQuestionTest(BasicTest):

    def test_standard(self):
        self.client.set_cookie('surveys/url-1', 'CLIENT_ID', 'cookie')
        future = self.make_future_get_request(f'{QUESTIONS_ENDPOINT}{str(self.example_ids[1])}')
        # get one question
        request = self.server.receives()
        request.ok(cursor={'id': 0, 'firstBatch': [{
            "_id": self.example_ids[0],
            "title": "example-title",
            "description": "example_description",
            "number": 1,
            'author': {"host": "localhost", "cookie": "cookie"},
            "url": "url",
            "date": self.sample_timestamp(),
            "questions": [
                {
                    "content": "example-content",
                    "reply": "reply",
                    'author': {"host": "localhost", "cookie": "cookie"},
                    "date": self.sample_timestamp(),
                    "votes": [{
                        'author': {"host": "localhost", "cookie": "cookie"},
                        "id": self.example_ids[2],
                        "date": self.sample_timestamp(),
                        "upvote": True
                    }],
                    "_id": self.example_ids[1],
                    "hidden": False
                }
            ]}]})

        http_response = future()
        self.assertEqual(http_response.status_code, HTTPStatus.OK)
        data = json.loads(http_response.get_data(as_text=True))
        self.assertEqual(data, {
            '_id': str(self.example_ids[1]),
            'content': 'example-content',
            'isAuthor': True,
            'voted': 'up',
            "reply": "reply",
            'downvotes': 0,
            'upvotes': 1,
            'votes': [{'upvote': True, 'date': self.sample_timestamp_string()}],
            'read': 'false',
            'hidden': False,
            'isAnonymous': True,
            'authorEmail': None,
            'authorFullName': None,
            'author_nickname': None
        })

    def test_notFound(self):
        future = self.make_future_get_request(f'{QUESTIONS_ENDPOINT}{str(self.example_ids[1])}')
        # get one question
        request = self.server.receives()
        request.ok(cursor={'id': 0, 'firstBatch': []})

        http_response = future()
        self.assertEqual(http_response.status_code, HTTPStatus.NOT_FOUND)

    def test_serverIssue(self):
        def broken_get_question(question_id, user):
            raise ArithmeticError

        temp = bridges.api.logic.get_question
        bridges.api.logic.get_question = broken_get_question

        future = self.make_future_get_request(f'{QUESTIONS_ENDPOINT}{str(self.example_ids[1])}',
            json.dumps(dict(title="title")))
        http_response = future()

        bridges.api.logic.get_question = temp
        self.assertEqual(
            http_response.status_code,
            HTTPStatus.INTERNAL_SERVER_ERROR)
