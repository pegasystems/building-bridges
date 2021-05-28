import logging

from http import HTTPStatus
from typing import Dict, Tuple
from flask import request
from flask_restx import Resource, fields
from bridges.api.serializers import question, survey_secrets_parser
from bridges.api import logic
from bridges.api.restplus import api
from bridges.utils import dict_subset

log = logging.getLogger(__name__)

ns = api.namespace('surveys', description='Operations related to surveys')

surveyApi = {
    'title': fields.String(required=True, description='Title of the survey'),
    'results_secret': fields.String(required=True,
                                    description='Secret to get results of the survey'),
    'admin_secret': fields.String(required=True,
                                  description='Secret to get to the admin page of the survey'),
    'hideVotes': fields.Boolean(required=False, description='Hide votes from users', default=False),
    'open': fields.Boolean(required=False, description='Is survey active', default=True),
    'key': fields.String(readOnly=True, required=True, description='Uri key for the survey'),
    'date': fields.DateTime(description="Date of survey creation"),
    'questions': fields.List(fields.Nested(question)),
    'viewsNumber': fields.Integer(required=False,
                                  description='Number of unique viewers', default=False),
    'votersNumber': fields.Integer(required=False,
                                   description='Number of unique voters', default=False),
    'questionersNumber': fields.Integer(required=False,
                                        description='Number of unique people who asked questions',
                                        default=False),
}

survey_basic = api.model('Survey Title', dict_subset(
    surveyApi, {'title', 'hideVotes'}))
survey_creation = api.model(
    'Survey Creation', dict_subset(surveyApi, {'key', 'results_secret', 'admin_secret'}))
survey_state = api.model(
    'Survey State', dict_subset(surveyApi, {'open'}))
survey_details = api.inherit(
    'Survey Details', survey_basic, dict_subset(
        surveyApi, {
            'key', 'date', 'open', 'viewsNumber', 'votersNumber', 'questionersNumber'
        }
    )
)
survey_details_with_secrets = api.inherit(
    'Survey Details with secrets', survey_details, dict_subset(
        surveyApi, {
            'results_secret', 'admin_secret'
        }
    )
)
survey_details_with_questions = api.inherit(
    'Survey Details with Questions', survey_details, dict_subset(surveyApi, {'questions'}))

@ns.route('/')
class SurveyCollection(Resource):
    """
    Api points that operates on all surveys.
    """

    @api.marshal_with(survey_details)
    def get(self) -> Tuple[Dict, HTTPStatus]:
        """
        Returns all surveys with details.
        """

        return logic.get_all_surveys(), HTTPStatus.OK

    @api.expect(survey_basic, validate=True)
    @api.response(201, 'Survey successfully created.')
    @api.marshal_with(survey_creation)
    def post(self) -> Tuple[Dict, HTTPStatus]:
        """
        Creates a new survey
        """

        key_and_secrets = logic.create_survey(
            title=request.json["title"],
            hide_votes=request.json.get("hideVotes") or False,
            description=None,
            author=request.user)
        return key_and_secrets, HTTPStatus.CREATED


@ns.route('/my')
class MySurveyCollection(Resource):
    """
    Api points that operates on user surveys.
    """

    @api.marshal_with(survey_details_with_secrets)
    def get(self) -> Tuple[Dict, HTTPStatus]:
        """
        Returns user surveys with details and secret.
        """

        return logic.get_user_surveys(user=request.user), HTTPStatus.OK


@ns.route('/<string:url>')
@api.expect(survey_secrets_parser)
@api.response(404, 'Survey not found.')
class SurveyItem(Resource):
    """
    Api points that operates on single survey.
    """

    @api.marshal_with(survey_details_with_questions)
    def get(self, url: str) -> Tuple[Dict, HTTPStatus]:
        """
        Returns a single survey.
        """

        secret_args = survey_secrets_parser.parse_args(request)

        survey = logic.get_survey(url,
                                  secret_args['results_secret'],
                                  secret_args['admin_secret'],
                                  request.user), HTTPStatus.OK
        logic.add_view_if_not_exists(viewer=request.user, survey_url=url)
        return survey

    @api.expect(survey_state)
    @api.response(201, 'Survey state changed.')
    @api.marshal_with(survey_state)
    def put(self, url: str) -> Tuple[Dict, HTTPStatus]:
        """
        Sets survey state: open/closed
        """

        is_open = logic.set_survey_state(survey_url=url,
                                         is_open=request.json.get("open") or False,
                                         admin_hash=survey_secrets_parser
                                         .parse_args(request)['admin_secret'])
        return is_open, HTTPStatus.CREATED
