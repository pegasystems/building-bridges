import json
from http import HTTPStatus
from unittest.mock import patch

from bridges.tests.api.basic_test import BasicTest

USER1 = {'host': 'host1.example.com', 'cookie': 'cookie1', 'user_id': 'abcdefghijklmnop'}
USER2 = {'host': 'host2.example.com', 'cookie': 'cookie2', 'user_id': 'abcdefghijklmnop'}
USER3 = {'host': 'host3.example.com', 'cookie': 'cookie3', 'user_id': 'qrstuvwxy987654321'}
USER4 = {'host': 'host3.example.com', 'cookie': 'cookie3', 'user_id': 'njnkajdaj812721811',
         'full_name': 'John Doe', 'email': 'john.doe@company.com'}


class GetSurveysTest(BasicTest):

    def handle_db_new_views(self):
        # get user view
        request = self.server.receives()
        request.ok(cursor={'id': 0, 'firstBatch': []})

        # add one view
        request = self.server.receives()
        request.ok({"nModified": 1})

    def test_standard(self):
        future = self.make_future_get_request('surveys/url-1')
        # get one survey
        request = self.server.receives()
        request.ok(cursor={'id': 0, 'firstBatch': [{
            "_id": self.example_ids[0],
            "title": "example-title",
            "description": "example_description",
            "number": 1,
            "hide_votes": False,
            "is_anonymous": True,
            'asking_questions_enabled': True,
            'voting_enabled': True,
            "results_secret": "secret",
            "admin_secret": "admin-secret",
            "views": [USER1],
            'author': {"host": "localhost", "cookie": "cookie"},
            "url": "example-url",
            "date": self.sample_timestamp(),
            "questions": [
                {
                    "content": "example-content-1",
                    'author': {"host": "localhost", "cookie": "cookie"},
                    "reply": 'sample reply',
                    "date": self.sample_timestamp(),
                    "votes": [],
                    "_id": self.example_ids[1],
                    "hidden": False
                },
                {
                    "content": "example-content-2",
                    'author': {"host": "localhost", "cookie": "cookie"},
                    "date": self.sample_timestamp(),
                    "votes": [
                        {'author': {"host": "localhost", "cookie": "cookie"},
                         'date': self.sample_timestamp(),
                         'upvote': True
                         }
                    ],
                    "_id": self.example_ids[2],
                    "hidden": False
                },
                {
                    "content": "example-content-3",
                    'author': {"host": "localhost", "cookie": "cookie"},
                    "date": self.sample_timestamp(),
                    "votes": [
                        {'author': {"host": "localhost", "cookie": "cookie"},
                         'date': self.sample_timestamp(),
                         'upvote': False
                         }
                    ],
                    "_id": self.example_ids[3],
                    "hidden": False
                }
            ]}]})

        self.handle_db_new_views()

        http_response = future()
        self.assertEqual(http_response.status_code, HTTPStatus.OK)
        data = json.loads(http_response.get_data(as_text=True))
        self.assertEqual(data, {
            "title": "example-title",
            "key": "example-url-1",
            "description": "example_description",
            "hideVotes": False,
            "isAnonymous": True,
            'question_author_name_field_visible': False,
            'limit_question_characters': 200,
            'limit_question_characters_enabled': False,
            'asking_questions_enabled': True,
            'voting_enabled': True,
            "viewsNumber": 1,
            "votersNumber": 1,
            "questionersNumber": 1,
            "date": self.sample_timestamp_string(),
            "questions": [
                {
                    "_id": str(self.example_ids[1]),
                    "content": "example-content-1",
                    "reply": 'sample reply',
                    "upvotes": 0,
                    "downvotes": 0,
                    "isAuthor": True,
                    "voted": "none",
                    "read": "false",
                    "hidden": False,
                    "isAnonymous": True,
                    "authorEmail": None,
                    "authorFullName": None,
                    'author_nickname': None
                },
                {
                    "_id": str(self.example_ids[2]),
                    "content": "example-content-2",
                    "reply": '',
                    "upvotes": 1,
                    "downvotes": 0,
                    "isAuthor": True,
                    "voted": "up",
                    "read": "false",
                    "hidden": False,
                    "isAnonymous": True,
                    "authorEmail": None,
                    "authorFullName": None,
                    'author_nickname': None
                },
                {
                    "_id": str(self.example_ids[3]),
                    "content": "example-content-3",
                    "reply": '',
                    "upvotes": 0,
                    "downvotes": 1,
                    "isAuthor": True,
                    "voted": "down",
                    "read": "false",
                    "hidden": False,
                    "isAnonymous": True,
                    "authorEmail": None,
                    "authorFullName": None,
                    'author_nickname': None
                },
            ]
        })

    def test_not_anonymous_survey_should_return_question_author_info(self):
        future = self.make_future_get_request('surveys/url-1')
        # get one survey
        request = self.server.receives()
        request.ok(cursor={'id': 0, 'firstBatch': [{
            "_id": self.example_ids[0],
            "title": "example-title",
            "description": "example_description",
            "number": 1,
            "hide_votes": False,
            "is_anonymous": False,
            "results_secret": "secret",
            "admin_secret": "admin-secret",
            "views": [USER4],
            'author': {"host": "localhost", "cookie": "cookie"},
            "url": "example-url",
            "date": self.sample_timestamp(),
            "questions": [
                {
                    "content": "example-content-1",
                    'author': USER4,
                    'reply': 'reply',
                    'is_anonymous': False,
                    "date": self.sample_timestamp(),
                    "votes": [],
                    "_id": self.example_ids[1],
                    "hidden": False
                },
            ]}]})

        self.handle_db_new_views()

        http_response = future()
        data = json.loads(http_response.get_data(as_text=True))
        self.assertEqual(data, {
            "title": "example-title",
            "key": "example-url-1",
            "description": "example_description",
            "hideVotes": False,
            "isAnonymous": False,
            'question_author_name_field_visible': False,
            'limit_question_characters': 200,
            'limit_question_characters_enabled': False,
            'asking_questions_enabled': True,
            'voting_enabled': True,
            "viewsNumber": 1,
            "votersNumber": 0,
            "questionersNumber": 1,
            "date": self.sample_timestamp_string(),
            "questions": [
                {
                    "_id": str(self.example_ids[1]),
                    "content": "example-content-1",
                    'reply': 'reply',
                    "upvotes": 0,
                    "downvotes": 0,
                    "isAuthor": False,
                    "voted": "none",
                    "read": "false",
                    "hidden": False,
                    "isAnonymous": False,
                    "authorEmail": USER4['email'],
                    "authorFullName": USER4['full_name'],
                    'author_nickname': None
                },
            ]
        })

    def test_hidden_votes(self):
        future = self.make_future_get_request('surveys/url-1')
        request = self.server.receives()
        request.ok(cursor={'id': 0, 'firstBatch': [{
            "_id": self.example_ids[0],
            "title": "example-title",
            "number": 1,
            "hide_votes": True,
            "isAnonymous": True,
            'question_author_name_field_visible': False,
            'asking_questions_enabled': True,
            'voting_enabled': True,
            "results_secret": "secret",
            "admin_secret": "admin-secret",
            "views": [USER1],
            'author': {
                "host": "NOT-LOCALHOST",
                "cookie": "BAD_COOKIE"
            },
            "url": "example-url",
            "date": self.sample_timestamp(),
            "questions": [
                {
                    "content": "example-content-2",
                    'author': {"host": "NOT-LOCALHOST", "cookie": "BAD_COOKIE"},
                    "date": self.sample_timestamp(),
                    "votes": [
                        {'author': {"host": "NOT-LOCALHOST", "cookie": "BAD_COOKIE"},
                         'date': self.sample_timestamp(),
                         'upvote': True
                         }
                    ],
                    "_id": self.example_ids[2],
                    "hidden": False,
                    "isAnonymous": True
                },
            ]}]})

        self.handle_db_new_views()

        http_response = future()
        self.assertEqual(http_response.status_code, HTTPStatus.OK)
        data = json.loads(http_response.get_data(as_text=True))
        self.assertEqual(data, {
            "title": "example-title",
            "key": "example-url-1",
            "hideVotes": True,
            "isAnonymous": True,
            "description": None,
            'question_author_name_field_visible': False,
            'limit_question_characters': 200,
            'limit_question_characters_enabled': False,
            'asking_questions_enabled': True,
            'voting_enabled': True,
            "viewsNumber": 1, "votersNumber": 1, "questionersNumber": 1,
            "date": self.sample_timestamp_string(),
            "questions": [
                {
                    "_id": str(self.example_ids[2]),
                    "authorEmail": None,
                    "authorFullName": None,
                    "reply": "",
                    'author_nickname': None,
                    "content": "example-content-2",
                    "upvotes": None,
                    "downvotes": None,
                    "isAuthor": False,
                    "voted": "none",
                    "read": "false",
                    "hidden": False,
                    "isAnonymous": True
                },
            ]
        })

    def test_hidden_votes_secrets(self):
        db_response = [{
            "_id": self.example_ids[0],
            "title": "example-title",
            "description": "example_description",
            "number": 1,
            "hide_votes": False,
            "isAnonymous": True,
            'asking_questions_enabled': True,
            'voting_enabled': True,
            "results_secret": "secret",
            "admin_secret": "admin-secret",
            'author': {"host": "NOT-LOCALHOST", "cookie": "BAD_COOKIE"},
            "url": "example-url",
            "date": self.sample_timestamp(),
            "views": [USER1, USER3],
            "questions": [
                {
                    "content": "example-content-2",
                    'author': {"host": "NOT-LOCALHOST", "cookie": "BAD_COOKIE"},
                    "reply": "answer",
                    "date": self.sample_timestamp(),
                    "votes": [
                        {'author': USER1,
                         'date': self.sample_timestamp(),
                         'upvote': True
                         },
                        {'author': USER2,
                         'date': self.sample_timestamp(),
                         'upvote': False
                         },
                        {'author': USER3,
                         'date': self.sample_timestamp(),
                         'upvote': False
                         }
                    ],
                    "voted": "none",
                    "_id": self.example_ids[2],
                    "hidden": False
                },
            ]}]

        api_correct_secret_response = {
            "title": "example-title",
            "key": "example-url-1",
            "hideVotes": False,
            "isAnonymous": True,
            "description": "example_description",
            'question_author_name_field_visible': False,
            'limit_question_characters': 200,
            'limit_question_characters_enabled': False,
            'asking_questions_enabled': True,
            'voting_enabled': True,
            "viewsNumber": 2, "votersNumber": 2, "questionersNumber": 1,
            "date": self.sample_timestamp_string(),
            "questions": [
                {
                    "_id": str(self.example_ids[2]),
                    "content": "example-content-2",
                    "upvotes": 1,
                    "downvotes": 2,
                    "reply": "answer",
                    "isAuthor": False,
                    "voted": "none",
                    "read": "false",
                    "hidden": False,
                    "isAnonymous": True,
                    "authorEmail": None,
                    "authorFullName": None,
                    'author_nickname': None
                },
            ]
        }

        def handle_correct_secret(url):
            future = self.make_future_get_request(url)
            request = self.server.receives()
            request.ok(cursor={'id': 0, 'firstBatch': db_response})
            self.handle_db_new_views()
            http_response = future()
            self.assertEqual(http_response.status_code, HTTPStatus.OK)
            data = json.loads(http_response.get_data(as_text=True))
            self.assertEqual(data, api_correct_secret_response)

        def test_hidden_votes_wrong_admin_secret():
            future = self.make_future_get_request('surveys/url-1?admin_secret=wrong-admin-secret')
            request = self.server.receives()
            request.ok(cursor={'id': 0, 'firstBatch': db_response})
            http_response = future()
            self.assertEqual(http_response.status_code, HTTPStatus.UNAUTHORIZED)

        def test_hidden_votes_with_admin_secret():
            handle_correct_secret('surveys/url-1?admin_secret=admin-secret')

        def test_hidden_votes_with_results_secret():
            handle_correct_secret('surveys/url-1?results_secret=secret')

        test_hidden_votes_with_admin_secret()
        test_hidden_votes_with_results_secret()
        test_hidden_votes_wrong_admin_secret()

    def test_notFound(self):
        future = self.make_future_get_request('surveys/not-existing-url-1')
        # get one survey
        request = self.server.receives()
        request.ok(cursor={'id': 0, 'firstBatch': []})
        http_response = future()
        self.assertEqual(http_response.status_code, HTTPStatus.NOT_FOUND)

    def test_badUrl(self):
        future = self.make_future_get_request('surveys/someVeryBadUrlWithoutNumber')
        # get one survey
        http_response = future()
        self.assertEqual(http_response.status_code, HTTPStatus.NOT_FOUND)

    def test_badUrlWithDashAtEnd(self):
        future = self.make_future_get_request('surveys/someVeryBadUrlWithoutNumber-')
        # get one survey
        http_response = future()
        self.assertEqual(http_response.status_code, HTTPStatus.NOT_FOUND)
