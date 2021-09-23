import json
from http import HTTPStatus

from bridges.tests.api.basic_test import BasicTest

SURVEYS_ENDPOINT = "surveys/"
USER1 = {'host': 'host1.example.com', 'cookie': 'cookie1'}
USER2 = {'host': 'host2.example.com', 'cookie': 'cookie2'}
USER3 = {'host': 'host3.example.com', 'cookie': 'cookie3'}


class GetSurveysTest(BasicTest):

    def test_empty(self):
        future = self.make_future_get_request(SURVEYS_ENDPOINT)
        # get all surveys
        request = self.server.receives()
        request.ok(cursor={'id': 0, 'firstBatch': []})

        http_response = future()
        self.assertEqual(http_response.status_code, HTTPStatus.OK)
        data = json.loads(http_response.get_data(as_text=True))
        self.assertEqual(data, [])

    def test_manySurveys(self):
        future = self.make_future_get_request(SURVEYS_ENDPOINT)
        # get all surveys
        request = self.server.receives()
        request.ok(cursor={'id': 0, 'firstBatch': [
            {
                'title': 'title1',
                'url': 'url',
                'date': self.sample_timestamp(),
                'number': 2,
                'hide_votes': False,
                'isAnonymous': True,
                'asking_questions_enabled': True,
                'voting_enabled': True,
                'author': {
                    "host": "host",
                    "cookie": "cookie"
                },
                "_id": self.example_ids[0],
                'questions': [
                    {
                        'content': 'Q1?',
                        'author': USER1,
                        'votes': [
                            {
                                'author': USER2,
                                'upvote': False
                            }
                        ]
                    }
                ],
                "secret": "SECRET",
                'views': [
                    USER1,
                    USER2
                ]
            },
            {
                'title': 'title2',
                'url': 'testurl',
                'date': self.sample_timestamp(),
                'number': 3,
                'hide_votes': True,
                'isAnonymous': True,
                'asking_questions_enabled': True,
                'voting_enabled': True,
                'author': {
                    "host": "host",
                    "cookie": "cookie"
                },
                "_id": self.example_ids[1],
                'description': 'desc',
                'questions': [
                    {
                        'content': 'Q1?',
                        'author': USER2,
                        'votes': [
                            {'author': USER2, 'upvote': False}
                        ]
                    },
                    {
                        'content': 'Q2?',
                        'author': USER1,
                        'reply': 'sample reply',
                        'votes': [
                             {
                                 'author': USER2,
                                 'upvote': False},
                             {
                                 'author': USER3,
                                 'upvote': True
                             }
                        ]
                    }
                ],
                "secret": "SECRET",
                'views': [
                    USER1
                ]
            }
        ]})
        http_response = future()
        self.assertEqual(http_response.status_code, HTTPStatus.OK)
        data = json.loads(http_response.get_data(as_text=True))
        self.assertEqual(data, [
            {
                'title': 'title1',
                'key': 'url-2',
                'date': self.sample_timestamp_string(),
                'description': None,
                'hideVotes': False,
                'isAnonymous': True,
                'question_author_name_field_visible': False,
                'limit_question_characters': 200,
                'limit_question_characters_enabled': False,
                'asking_questions_enabled': True,
                'voting_enabled': True,
                'viewsNumber': 2,
                'votersNumber': 1,
                'questionersNumber': 1
            },
            {
                'title': 'title2',
                'key': 'testurl-3',
                'date': self.sample_timestamp_string(),
                'description': 'desc',
                'hideVotes': True,
                'isAnonymous': True,
                'question_author_name_field_visible': False,
                'limit_question_characters': 200,
                'limit_question_characters_enabled': False,
                'asking_questions_enabled': True,
                'voting_enabled': True,
                'viewsNumber': 1,
                'votersNumber': 2,
                'questionersNumber': 2
            }
        ])

    def test_my(self):
        future = self.make_future_get_request(SURVEYS_ENDPOINT + "my")
        # get all surveys
        request = self.server.receives()
        request.ok(cursor={'id': 0, 'firstBatch': [
            {
                'title': 'title1',
                'url': 'url',
                'date': self.sample_timestamp(),
                'number': 2,
                'hide_votes': False,
                'isAnonymous': True,
                'question_author_name_field_visible': False,
                'asking_questions_enabled': True,
                'voting_enabled': True,
                'author': {
                    "host": "localhost",
                    "cookie": "cookie"
                },
                "_id": self.example_ids[0],
                'description': 'desc',
                'questions': [
                    {
                        'content': 'Q1?',
                        'author': USER3,
                        'votes': [
                            {
                                'author': USER1,
                                'upvote': False
                            }
                        ]
                    },
                    {
                        'content': 'Q2?',
                        'author': USER1,
                        'votes': [
                            {
                                'author': USER2,
                                'upvote': False
                            },
                            {
                                'author': USER3,
                                'upvote': True
                            }
                        ]
                    }
                ],
                "admin_secret": "SECRET",
                "results_secret": "SECRET",
                'views': [
                    USER1,
                    USER2,
                    USER3
                ]
            },
        ]})
        http_response = future()
        self.assertEqual(http_response.status_code, HTTPStatus.OK)
        data = json.loads(http_response.get_data(as_text=True))
        self.assertEqual(data, [
            {
                'title': 'title1',
                'key': 'url-2',
                'date': self.sample_timestamp_string(),
                'description': 'desc',
                'hideVotes': False,
                'isAnonymous': True,
                'viewsNumber': 3,
                'votersNumber': 3,
                'questionersNumber': 2,
                'question_author_name_field_visible': False,
                'limit_question_characters': 200,
                'limit_question_characters_enabled': False,
                'asking_questions_enabled': True,
                'voting_enabled': True,
                'results_secret': 'SECRET',
                'admin_secret': 'SECRET'
            }
        ])
