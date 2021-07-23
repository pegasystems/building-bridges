import logging

from http import HTTPStatus
from typing import Tuple, Dict
from flask import request
from flask_restx import fields
from flask_restx import Resource
from bridges.api import logic
from bridges.api.question_model import question_model_dict, question
from bridges.api.restplus import api
from bridges.api import surveys
from bridges.api.surveys import survey_secrets
from bridges.database.objects.survey import Survey
from bridges.errors import QuestionRemovingError
from bridges.utils import dict_subset


log = logging.getLogger(__name__)

ns = api.namespace(
    'surveys',
    description='Operations related to surveys')

votes = api.model('Votes', {
    'upvote': fields.Boolean(
        required=True,
        description='Is vote an upvote'),
    'date': fields.DateTime(
        description="Date of the vote")
})

question_id_model = api.model("Question id", dict_subset(question_model_dict, {
    '_id'
}))

question_details_model = api.inherit("Question's details", question, {
    'votes': fields.List(fields.Nested(votes))
})

post_question_model = api.model("Post question", {
    'content': fields.String(
        required=True,
        description='Content of the question')
})

question_state_model = api.model(
    'Question State', dict_subset(question_model_dict, {
        'hidden'
    }))

@ns.route('/<string:survey_url>/questions')
class QuestionCollection(Resource):
    """
    Api points that operates on all the questions
    in one survey.
    """

    @api.expect(post_question_model, validate=True)
    @api.marshal_with(question_id_model)
    @surveys.survey_api.get
    @surveys.survey_api.asking_questions_enabled
    def post(self, survey: Survey) -> Tuple[Dict, int]:
        """
        Add new question
        """

        return {
            "_id": str(logic.add_question(
                survey=survey,
                question=request.json["content"],
                user=request.user))
        }, HTTPStatus.CREATED


@ns.route('/<string:survey_url>/questions/<string:question_id>')
@api.expect(survey_secrets)
@api.response(404, 'Question not found.')
class QuestionItem(Resource):
    """
    Api points that operates on single question in one survey.
    """

    @api.marshal_with(question_details_model)
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

    @api.expect(question_state_model)
    @api.response(201, 'Question state changed.')
    @api.marshal_with(question_state_model)
    def put(self, survey_url: str,
               question_id: str) -> Tuple[Dict, HTTPStatus]:
        """
        Hides a single question in survey
        """

        logic.set_question_state(
                    survey_url=survey_url,
                    question_id=question_id,
                    hidden=request.json.get("hidden") or False,
                    admin_hash=survey_secrets
                    .parse_args(request)['admin_secret'])
        return None, HTTPStatus.OK
