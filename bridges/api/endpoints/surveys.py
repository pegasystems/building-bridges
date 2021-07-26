import logging

from flask_restx import reqparse
from http import HTTPStatus
from typing import Dict, Tuple, Callable
from flask import request
from flask_restx import Resource, fields
from bridges.api import logic
from bridges.api.question_model import question
from bridges.api.restplus import api
from bridges.database.objects.survey import Survey
from bridges.errors import UnauthorizedError
from bridges.utils import dict_subset
import bridges.database.mongo as db

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
    'open': fields.Boolean(
        required=False,
        description='Is survey active',
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
        description='Number of unique viewers',
        default=False),
    'votersNumber': fields.Integer(
        required=False,
        description='Number of unique voters',
        default=False),
    'questionersNumber': fields.Integer(
        required=False,
        description='Number of unique people who asked questions',
        default=False),
    'error': fields.String(
        readOnly=True,
        required=False,
        description='Message in case of error'),
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
        'open',
        'error'
    }))

survey_details_model = api.inherit(
    'Survey Details', survey_basic_model, dict_subset(
        survey_model, {
            'key',
            'date',
            'open',
            'viewsNumber',
            'votersNumber',
            'questionersNumber'
        }
    )
)

survey_details_with_secrets_model = api.inherit(
    'Survey Details with secrets', survey_details_model, dict_subset(
        survey_model, {
            'results_secret',
            'admin_secret'
        }
    )
)

survey_details_with_questions_model = api.inherit(
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
    def get(self) -> Tuple[Dict, HTTPStatus]:
        """
        Returns all surveys with details.
        """

        return logic.get_all_surveys(), HTTPStatus.OK

    @api.expect(survey_basic_model, validate=True)
    @api.response(201, 'Survey successfully created.')
    @api.marshal_with(survey_created_model)
    def post(self) -> Tuple[Dict, HTTPStatus]:
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

    @api.marshal_with(survey_details_with_secrets_model)
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

    @api.marshal_with(survey_details_with_questions_model)
    @survey_api.get
    def get(self, survey: Survey) -> Tuple[Dict, int]:
        """
        Returns a single survey.
        """

        secret_args = survey_secrets.parse_args(request)
        results_hash = secret_args['results_secret']
        admin_secret = secret_args['admin_secret']

        if not logic.is_secret_valid_if_provided(survey.results_secret, results_hash) or \
                not logic.is_secret_valid_if_provided(survey.admin_secret,admin_secret):
            raise UnauthorizedError("Wrong secret provided.")
        logic.add_view_if_not_exists(viewer=request.user, survey=survey)

        return survey.get_api_result(request.user, results_hash, admin_secret), HTTPStatus.OK

    @api.expect(survey_settings_model)
    @api.response(201, 'Survey settings changed.')
    @api.marshal_with(survey_settings_model)
    @survey_api.get
    @survey_api.admin
    def put(self, survey: Survey) -> Tuple[Dict, int]:
        """
        Change survey settings.
        """

        settings = ['open']
        settings_values = {s: request.json.get(s) for s in settings}
        settings_not_none = {key: value for (key, value) in settings_values.items() if value is not None}
        settings_changed = {key: value for (key, value) in settings_not_none.items() if value != survey.__getattribute__(key)}

        survey = db.update_survey(survey, settings_changed)

        return survey.__dict__, HTTPStatus.CREATED
