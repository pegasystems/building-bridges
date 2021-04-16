import logging

from http import HTTPStatus
from typing import Tuple, Dict
from flask import request
from flask_restx import Resource
from bridges.api.serializers import (
    post_question,
    detalic_question,
    question_id as question_id_model
)
from bridges.api import logic
from bridges.api.restplus import api
from bridges.errors import QuestionRemovingError


log = logging.getLogger(__name__)

ns = api.namespace('surveys', description='Operations related to surveys')


@ns.route('/<string:survey_url>/questions')
class QuestionCollection(Resource):
    """
    Api points that operates on all the questions
    in one survey.
    """

    @api.expect(post_question, validate=True)
    @api.marshal_with(question_id_model)
    def post(self, survey_url: str) -> Tuple[Dict, HTTPStatus]:
        """
        Add new question
        """
        kek = "asdadaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        return {
            "_id": str(logic.add_question(
                survey_url=survey_url,
                question=request.json["content"],
                user=request.user))
        }, HTTPStatus.CREATED


@ns.route('/<string:survey_url>/questions/<string:question_id>')
@api.response(404, 'Question not found.')
class QuestionItem(Resource):
    """
    Api points that operates on single question in one survey.
    """

    @api.marshal_with(detalic_question)
    def get(self, survey_url: str,
            question_id: str) -> Tuple[Dict, HTTPStatus]:
        """
        Returns a single question in survey
        """

        return logic.get_question(question_id=question_id, user=request.user)

    def delete(self, survey_url: str,
               question_id: str) -> Tuple[Dict, HTTPStatus]:
        """
        Deletes a single question in survey
        """

        try:
            logic.remove_question(question_id=question_id, survey_url=survey_url, user=request.user)
            return None, HTTPStatus.NO_CONTENT
        except QuestionRemovingError:
            return {
                "message": "Can't remove question that already has votes"}, HTTPStatus.FORBIDDEN
