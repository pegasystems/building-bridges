from flask_restx import reqparse
from flask_restx.reqparse import RequestParser


def create_put_question_parser() -> RequestParser:
    """
    We use this parser in the vote endpoint - we want to
    ensure, that only a possible type of vote is putted.
    """

    parser = reqparse.RequestParser()
    parser.add_argument(
        'type',
        type=str,
        required=True,
        help='The type of a vote',
        choices=[
            'up',
            'down'],
        location='args')
    return parser


def create_put_user_context_parser() -> RequestParser:
    """
    We use this parser in the vote endpoint - we want to
    ensure, that only a possible type of vote is putted.
    """

    parser = reqparse.RequestParser()
    parser.add_argument(
        'read',
        type=str,
        required=True,
        help='Mark as read state',
        choices=[
            'true',
            'false'],
        location='args')
    return parser


put_question_parser = create_put_question_parser()
put_user_context_parser = create_put_user_context_parser()
