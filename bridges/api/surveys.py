import logging

from flask import request
from flask_restx import Resource, reqparse, fields
from http import HTTPStatus
from typing import Callable, Tuple, List, Dict

import bridges.database.mongo as db
from bridges.api import logic
from bridges.api.question_model import question
from bridges.api.restplus import api
from bridges.database.objects.survey import Survey
from bridges.utils import dict_subset

log = logging.getLogger(__name__)

survey_secrets = reqparse.RequestParser()\
    \
    .add_argument(
    'results_secret',
    type=str,
    required=False,
    help='Secret to get full results of survey',
    location='args')\
    \
    .add_argument(
    'admin_secret',
    type=str,
    required=False,
    help='Secret to get to the admin page of survey',
    location='args')


class SurveyApi(object):

    @staticmethod
    def get(func) -> Callable:
        """
        Retrieve survey from database and pass it to decorated method.
        """
        def wrapper_get(*args, **kwargs):
            survey_url = kwargs['survey_url']
            survey = db.get_survey(survey_url)
            if survey is None:
                return {
                           'error': 'Survey not found'
                       }, HTTPStatus.NOT_FOUND
            return func(*args, survey=survey)

        return wrapper_get

    @staticmethod
    def admin(func):
        """
        Check if it is an admin of survey.
        """
        def wrapper_owner(*args, **kwargs):
            survey = kwargs['survey']
            admin_secret = survey_secrets.parse_args(request)['admin_secret']
            if survey.admin_secret != admin_secret:
                return {
                       'error': 'Not allowed.'
                       }, HTTPStatus.UNAUTHORIZED
            return func(*args, survey=survey)

        return wrapper_owner

    @staticmethod
    def asking_questions_enabled(func) -> Callable:
        """
        Validate if adding questions to given survey is open before executing operations on the survey.
        """
        def wrapper_asking_questions_enabled(*args, **kwargs):
            survey = kwargs['survey']
            if not survey.asking_questions_enabled:
                return {
                           'error': 'Asking questions not allowed for this survey'
                       }, HTTPStatus.METHOD_NOT_ALLOWED
            return func(*args, survey=survey)
        return wrapper_asking_questions_enabled

    @staticmethod
    def voting_enabled(func) -> Callable:
        """
        Validate if voting on questions is open before executing operations on the survey.
        """
        def wrapper_voting_enabled(*args, **kwargs):
            survey = kwargs['survey']
            if not survey.voting_enabled:
                return {
                           'error': 'Voting not allowed for this survey'
                       }, HTTPStatus.METHOD_NOT_ALLOWED
            return func(*args, survey=survey)

        return wrapper_voting_enabled


survey_api = SurveyApi()

ns = api.namespace('surveys', description='Operations related to surveys')

survey_model = {
    'title': fields.String(
        required=True,
        description='Title of the survey'),
    'results_secret': fields.String(
        required=True,
        description='Secret to get results of the survey'),
    'admin_secret': fields.String(
        required=True,
        description='Secret to get to the admin page of the survey'),
    'description': fields.String(
        required=False,
        description='Description of the survey'),
    'hideVotes': fields.Boolean(
        required=False,
        description='Hide votes from users',
        default=False),
    'askingQuestionsEnabled': fields.Boolean(
        required=False,
        description='Is adding question possible',
        default=True),
    'votingEnabled': fields.Boolean(
        required=False,
        description='Is voting possible',
        default=True),
    'key': fields.String(
        readOnly=True,
        required=True,
        description='Uri key for the survey'),
    'date': fields.DateTime(
        description="Date of survey creation"),
    'questions': fields.List(
        fields.Nested(question)),
    'viewsNumber': fields.Integer(
        required=False,
        description='Number of unique viewers', default=False),
    'votersNumber': fields.Integer(
        required=False,
        description='Number of unique voters', default=False),
    'questionersNumber': fields.Integer(
        required=False,
        description='Number of unique people who asked questions',
        default=False),
}

survey_basic_model = api.model(
    'Survey Title', dict_subset(survey_model, {
        'title',
        'hideVotes',
        'description'
    }))

survey_created_model = api.model(
    'Survey Created', dict_subset(survey_model, {
        'key',
        'results_secret',
        'admin_secret'
    }))

survey_settings_model = api.model(
    'Survey Settings', dict_subset(survey_model, {
        'askingQuestionsEnabled',
        'votingEnabled'
    }))

survey_details_model = api.inherit(
    'Survey Details', survey_basic_model, dict_subset(
        survey_model, {
            'key',
            'date',
            'allowAskingQuestions',
            'allowVoting',
            'viewsNumber',
            'votersNumber',
            'questionersNumber'
        }
    )
)

survey_details_with_secrets = api.inherit(
    'Survey Details with secrets', survey_details_model, dict_subset(
        survey_model, {
            'results_secret',
            'admin_secret'
        }
    )
)
survey_details_with_questions = api.inherit(
    'Survey Details with Questions', survey_details_model, dict_subset(
        survey_model, {
            'questions'
        }))


@ns.route('/')
class SurveyCollection(Resource):
    """
    Api points that operates on all surveys.
    """

    @api.marshal_with(survey_details_model)
    def get(self) -> Tuple[List[Dict], int]:
        """
        Returns all surveys with details.
        """

        return list(map(
            Survey.get_api_brief_result,
            db.get_all_surveys())), HTTPStatus.OK

    @api.expect(survey_basic_model, validate=True)
    @api.response(201, 'Survey successfully created.')
    @api.marshal_with(survey_created_model)
    def post(self) -> Tuple[Dict, int]:
        """
        Creates a new survey
        """

        key_and_secrets = logic.create_survey(
            title=request.json["title"],
            hide_votes=request.json.get("hideVotes") or False,
            description=request.json.get("description"),
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


@ns.route('/<string:survey_url>')
@api.expect(survey_secrets)
@api.response(404, 'Survey not found.')
class SurveyItem(Resource):
    """
    Api points that operates on single survey.
    """

    @api.marshal_with(survey_details_with_questions)
    @survey_api.get
    def get(self, survey: Survey) -> Tuple[Dict, HTTPStatus]:
        """
        Returns a single survey.
        """

        secret_args = survey_secrets.parse_args(request)

        # survey = logic.get_survey(survey_url,
        #                           secret_args['results_secret'],
        #                           secret_args['admin_secret'],
        #                           request.user), HTTPStatus.OK
        return survey

    @api.expect(survey_settings_model)
    @api.response(201, 'Survey state changed.')
    @api.marshal_with(survey_settings_model)
    @survey_api.get
    @survey_api.admin
    def update(self, survey: Survey) -> Tuple[Dict, HTTPStatus]:
        """
        Change survey settings.
        """

        is_open = logic.set_survey_settings(
            survey=survey,
            is_open=request.json.get("open") or False,
            admin_hash=survey_secrets
                .parse_args(request)['admin_secret'])
        return is_open, HTTPStatus.CREATED
