from flask_restx import fields, reqparse
from bridges.api.restplus import api
from bridges.utils import dict_subset


QUESTION_ID_DESCRIPTION = 'ID of the question'

votes = api.model('Votes', {
    'upvote': fields.Boolean(required=True, description='Is vote an upvote'),
    'date': fields.DateTime(description="Date of the vote")
})

question_model_dict = {
    '_id': fields.String(description=QUESTION_ID_DESCRIPTION),
    'content': fields.String(required=True, description='Content of the question'),
    'upvotes': fields.Integer(description='Number of upvotes in the question'),
    'downvotes': fields.Integer(description='Number of downvotes in the question'),
    'isAuthor': fields.Boolean(description='Is current user author of the question'),
    'voted': fields.String(description='How the current user voted on the question (up/down/none)'),
    'read': fields.String(description='If the current user marked question as read (true/false)'),
    'hidden': fields.Boolean(required=False, description='Is question hidden', default=False),
}

question = api.model('Question', question_model_dict)

question_id = api.model("Question id", dict_subset(question_model_dict, {'_id'}))

detalic_question = api.inherit('Detalic question', question, {
    'votes': fields.List(fields.Nested(votes))
})

question_state = api.model(
    'Question State', dict_subset(question_model_dict, {'hidden'}))

my_vote = api.model('My question', {
    'id': fields.String(description=QUESTION_ID_DESCRIPTION),
    'upvote': fields.Boolean(description='Is vote an upvote')
})

my_question = api.model('My question', {
    'id': fields.String(description=QUESTION_ID_DESCRIPTION),
})

post_question = api.model("Post question", {
    'content': fields.String(required=True, description='Content of the question')
})

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
