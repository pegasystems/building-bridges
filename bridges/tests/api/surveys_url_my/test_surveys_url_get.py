import json
from http import HTTPStatus
from unittest.mock import patch

from bridges.tests.api.basic_test import BasicTest

USER1 = {'host': 'host1.example.com', 'cookie': 'cookie1', 'user_id': 'abcdefghijklmnop'}
USER2 = {'host': 'host2.example.com', 'cookie': 'cookie2', 'user_id': 'abcdefghijklmnop'}
USER3 = {'host': 'host3.example.com', 'cookie': 'cookie3', 'user_id': 'qrstuvwxy987654321'}


class GetSurveysTest(BasicTest):

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
            'open': True,
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

        # get user view
        request = self.server.receives()
        request.ok(cursor={'id': 0, 'firstBatch': []})

        # add one view
        request = self.server.receives()
        request.ok({"nModified": 1})

        http_response = future()
        self.assertEqual(http_response.status_code, HTTPStatus.OK)
        data = json.loads(http_response.get_data(as_text=True))
        self.assertEqual(data, {
            "title": "example-title",
            "key": "example-url-1",
            "description": "example_description",
            "hideVotes": False,
            'open': True,
            'asking_questions_enabled': True,
            'voting_enabled': True,
            "viewsNumber": 1, "votersNumber": 1, "questionersNumber": 1,
            "date": self.sample_timestamp_string(),
            "questions": [
                {
                    "_id": str(self.example_ids[1]),
                    "content": "example-content-1",
                    "upvotes": 0,
                    "downvotes": 0,
                    "isAuthor": True,
                    "voted": "none",
                    "read": "false",
                    "hidden": False
                },
                {
                    "_id": str(self.example_ids[2]),
                    "content": "example-content-2",
                    "upvotes": 1,
                    "downvotes": 0,
                    "isAuthor": True,
                    "voted": "up",
                    "read": "false",
                    "hidden": False
                },
                {
                    "_id": str(self.example_ids[3]),
                    "content": "example-content-3",
                    "upvotes": 0,
                    "downvotes": 1,
                    "isAuthor": True,
                    "voted": "down",
                    "read": "false",
                    "hidden": False
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
            'open': True,
            'asking_questions_enabled': True,
            'voting_enabled': True,
            "results_secret": "secret",
            "admin_secret": "admin-secret",
            "views": [USER1],
            'author': {"host": "NOT-LOCALHOST", "cookie": "BAD_COOKIE"},
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
                    "hidden": False
                },
            ]}]})

        # get user view
        request = self.server.receives()
        request.ok(cursor={'id': 0, 'firstBatch': []})

        # add one view
        request = self.server.receives()
        request.ok({"nModified": 1})

        http_response = future()
        self.assertEqual(http_response.status_code, HTTPStatus.OK)
        data = json.loads(http_response.get_data(as_text=True))
        self.assertEqual(data, {
            "title": "example-title",
            "key": "example-url-1",
            "hideVotes": True,
            "description": None,
            'open': True,
            'asking_questions_enabled': True,
            'voting_enabled': True,
            "viewsNumber": 1, "votersNumber": 1, "questionersNumber": 1,
            "date": self.sample_timestamp_string(),
            "questions": [
                {
                    "_id": str(self.example_ids[2]),
                    "content": "example-content-2",
                    "upvotes": None,
                    "downvotes": None,
                    "isAuthor": False,
                    "voted": "none",
                    "read": "false",
                    "hidden": False
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
            'open': True,
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
            "description": "example_description",
            'open': True,
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
                    "isAuthor": False,
                    "voted": "none",
                    "read": "false",
                    "hidden": False
                },
            ]
        }

        def handle_db_new_views(self):
            # get user view
            request = self.server.receives()
            request.ok(cursor={'id': 0, 'firstBatch': []})

            # add one view
            request = self.server.receives()
            request.ok({"nModified": 1})

        def handle_correct_secret(url):
            future = self.make_future_get_request(url)
            request = self.server.receives()
            request.ok(cursor={'id': 0, 'firstBatch': db_response})
            handle_db_new_views(self)
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
