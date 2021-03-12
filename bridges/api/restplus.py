import logging
import traceback
import json

from http import HTTPStatus
from typing import Tuple, Dict
from flask_restx import Api
from werkzeug.exceptions import BadRequest
from bridges.errors import NotFoundError, BadUrlError, UnauthorizedError, BadQuestionError, \
    SurveyClosedError
from bridges.argument_parser import args


log = logging.getLogger(__name__)

api = Api(version='1.0', title='Building bridges API',
          description='API for building bridges')


@api.errorhandler(Exception)
def default_error_handler(e: Exception) -> Tuple[Dict, HTTPStatus]:
    """
    If any unhandled exception occur during the API call,
    it will be handled by this function.
    """

    error_to_result = {
        BadRequest: HTTPStatus.BAD_REQUEST,
        NotFoundError: HTTPStatus.NOT_FOUND,
        UnauthorizedError: HTTPStatus.UNAUTHORIZED,
        BadUrlError: HTTPStatus.NOT_FOUND,
        BadQuestionError: HTTPStatus.BAD_REQUEST,
        SurveyClosedError: HTTPStatus.METHOD_NOT_ALLOWED
    }

    for error, result in error_to_result.items():
        if isinstance(e, error):
            return {'message': str(e)}, result

    log.exception(e)
    return (({'message': json.dumps(
        traceback.format_exc())}, HTTPStatus.INTERNAL_SERVER_ERROR) if args.debug
            else ({'message': 'An unhandled exception occurred.'},
                  HTTPStatus.INTERNAL_SERVER_ERROR))
