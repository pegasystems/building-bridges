import logging

from http import HTTPStatus
from typing import Dict, Tuple
from flask import request
from flask_restx import Resource
from bridges.api.parse_args import put_user_context_parser
from bridges.api import logic
from bridges.api.restplus import api


log = logging.getLogger(__name__)

ns = api.namespace('surveys', description='Operations related to surveys')


@ns.route('/<string:survey_url>/questions/<string:question_id>/ctx')
class UserContextCollection(Resource):
    """
    Api points that operates on votes collection
    in one question.
    """

    def put(self, survey_url: str, question_id: str) -> Tuple[Dict, int]:
        """
        Add new read state
        """
        logic.mark_as_read(
            question_id=question_id,
            survey_url=survey_url,
            user=request.user,
            is_read=put_user_context_parser.parse_args(request)['read']
        )
        return None, HTTPStatus.CREATED
