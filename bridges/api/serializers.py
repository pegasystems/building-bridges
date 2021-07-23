from flask_restx import fields, reqparse
from bridges.api.restplus import api

survey_secrets_parser = reqparse.RequestParser()
survey_secrets_parser.add_argument(
    'results_secret',
    type=str,
    required=False,
    help='Secret to get full results of survey',
    location='args')
survey_secrets_parser.add_argument(
    'admin_secret',
    type=str,
    required=False,
    help='Secret to get to the admin page of survey',
    location='args')
