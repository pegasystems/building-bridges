import logging

from http import HTTPStatus
from typing import Dict, Tuple
from flask import request
from flask_restx import Resource, fields


from bridges.api.endpoints.surveys import survey_api
from bridges.api.parse_args import put_question_parser
from bridges.api import logic
from bridges.database.objects.survey import Survey
from bridges.api.restplus import api
from bridges.utils import dict_subset
from bridges.api.question_model import question_model_dict

log = logging.getLogger(__name__)

ns = api.namespace('surveys', description='Operations related to surveys')

reply_model = api.model("Reply to question", {
    'content': fields.String(
        required=True,
        description='Content of the question')
    }
)

@ns.route('/<string:survey_url>/questions/<string:question_id>/reply')
class Reply(Resource):
    """
    Api points that operates on reply
    in one question.
    """

    @api.expect(reply_model, validate=True)
    @survey_api.get
    @survey_api.admin
    def put(self, survey: Survey, question_id: str) -> Tuple[Dict, int]:
        """
        Add new response
        """
        logic.set_reply(
            question_id=question_id,
            content=request.json.get("content")
        )
        return None, HTTPStatus.CREATED
