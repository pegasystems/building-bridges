import json
from http import HTTPStatus

from mockupdb import MockupDB, go, Command, OpReply
from json import dumps
import datetime
from bridges.tests.api.basic_test import BasicTest
import bridges.api.logic

QUESTIONS_ENDPOINT = 'surveys/test-1/questions'
QUESTIONS_CONTENT = "question content"


class PostQuestionTest(BasicTest):
    def test_normal(self):
        future = self.make_future_post_request(QUESTIONS_ENDPOINT, dict(
            content=QUESTIONS_CONTENT))
        # get data about survey
        self.mock_get_info_about_survey()
        self.mock_get_info_about_survey()
        # update one survey - add question into it
        request = self.server.receives()
        request.ok({"nModified": 1})
        http_response = future()
        self.assertEqual(http_response.status_code, HTTPStatus.CREATED)

    def test_not_add_question_to_disabled_survey(self):
        future = self.make_future_post_request(QUESTIONS_ENDPOINT, dict(
            content=QUESTIONS_CONTENT))
        # get data about survey
        self.mock_get_info_about_survey(asking_questions_enabled=False)
        http_response = future()
        self.assertEqual(http_response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

    def test_bad_request(self):
        future = self.make_future_post_request(QUESTIONS_ENDPOINT, dict(
            bad_content_key=QUESTIONS_CONTENT))
        http_response = future()
        self.assertEqual(http_response.status_code, HTTPStatus.BAD_REQUEST)

    def test_surveyNotFound(self):
        future = self.make_future_post_request(QUESTIONS_ENDPOINT, dict(
            content=QUESTIONS_CONTENT))
        # get data about non-existing survey
        request = self.server.receives()
        request.ok(cursor={'id': 0, 'firstBatch': []})
        # tries to add question to one survey
        request = self.server.receives()
        request.ok({'nModified': 0})
        http_response = future()
        self.assertEqual(http_response.status_code, HTTPStatus.NOT_FOUND)

    def test_overpass_character_limit(self):
        future = self.make_future_post_request(f'{QUESTIONS_ENDPOINT}',
                                               dict(content='123456'))
        # get data about survey
        self.mock_get_info_about_survey(
            limit_question_characters_enabled=True,
            limit_question_characters=5)
        http_response = future()
        self.assertEqual(http_response.status_code, HTTPStatus.BAD_REQUEST)
