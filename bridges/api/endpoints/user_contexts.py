import logging

from http import HTTPStatus
from typing import Dict, Tuple
from flask import request
from flask_restx import Resource

from bridges.api.endpoints.surveys import survey_api
from bridges.api.parse_args import put_user_context_parser
from bridges.api import logic
from bridges.api.restplus import api
from bridges.database.objects.survey import Survey

log = logging.getLogger(__name__)

ns = api.namespace('surveys', description='Operations related to surveys')


@ns.route('/<string:survey_url>/questions/<string:question_id>/ctx')
class UserContextCollection(Resource):
    """
    Api points that operates on votes collection
    in one question.
    """

    @survey_api.get
    @survey_api.asking_questions_enabled
    def put(self, survey: Survey, question_id: str) -> Tuple[Dict, int]:
        """
        Add new read state
        """
        logic.mark_as_read(
            question_id=question_id,
            user=request.user,
            is_read=put_user_context_parser.parse_args(request)['read']
        )
        return None, HTTPStatus.CREATED
