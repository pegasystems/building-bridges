import logging

from http import HTTPStatus
from typing import Dict, Tuple
from flask import request
from flask_restx import Resource

from bridges.api.endpoints.surveys import survey_api
from bridges.api.parse_args import put_question_parser
from bridges.api import logic
from bridges.api.restplus import api
from bridges.database.objects.survey import Survey

log = logging.getLogger(__name__)

ns = api.namespace('surveys', description='Operations related to surveys')


@ns.route('/<string:survey_url>/questions/<string:question_id>/vote')
class VotesCollection(Resource):
    """
    Api points that operates on votes collection
    in one question.
    """

    @api.expect(put_question_parser, validate=True)

    @survey_api.voting_enabled
    def put(self, question_id: str) -> Tuple[Dict, int]:
        """
        Add new vote
        """
        logic.add_vote(
            question_id=question_id,
            user=request.user,
            is_upvote=put_question_parser.parse_args(request)['type'] == 'up')
        return None, HTTPStatus.CREATED

    @survey_api.voting_enabled
    def delete(self, question_id: str) -> Tuple[Dict, int]:
        """
        Delete vote
        """
        logic.delete_vote(question_id=question_id, user=request.user)
        return None, HTTPStatus.NO_CONTENT
