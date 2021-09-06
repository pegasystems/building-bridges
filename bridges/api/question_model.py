from flask_restx import fields

from bridges.api.restplus import api

question_model_dict = {
    '_id': fields.String(
        description='ID of the question'),
    'content': fields.String(
        required=True,
        description='Content of the question'),
    'upvotes': fields.Integer(
        description='Number of upvotes in the question'),
    'downvotes': fields.Integer(
        description='Number of downvotes in the question'),
    'isAuthor': fields.Boolean(
        description='Is current user author of the question'),
    'isAnonymous': fields.Boolean(
        description='Is author of the question anonymous'),
    'authorFullName': fields.String(
        description='Full name of the question author'),
    'authorEmail': fields.String(
        description='E-mail of the question author'),
    'author_nickname': fields.String(
        required=False,
        description='Name put by author'),
    'voted': fields.String(
        description='How the current user voted on the question (up/down/none)'),
    'read': fields.String(
        description='If the current user marked question as read (true/false)'),
    'hidden': fields.Boolean(
        required=False,
        description='Is question hidden',
        default=False),
}

question = api.model('Question', question_model_dict)