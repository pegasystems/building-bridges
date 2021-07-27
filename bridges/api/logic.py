import secrets

from typing import List, Dict
from bson.objectid import ObjectId

import bridges.database.mongo as db
from bridges.database.objects.question import Question
from bridges.errors import NotFoundError, UnauthorizedError, QuestionRemovingError, \
    BadQuestionError, SurveyClosedError
from bridges.utils import sanitize
from bridges.database.objects.survey import Survey
from bridges.database.objects.user import User


SURVEY_NOT_FOUND_ERROR_MESSAGE = "Survey not found."


def is_secret_valid_if_provided(server_secret: str, user_provided_secret: str):
    if not user_provided_secret:
        return True
    return server_secret == user_provided_secret


def anonymize_user(func):
    """
    Make sure authenticated user remains anonymous before executing operations;
    if the wrapped method has keyword argument of type 'User',
    it clears all user's sensitive data.
    """
    def wrapper_anonymize_user(*args, **kwargs):
        user_key = next((k for k in kwargs.keys() if isinstance(kwargs[k], User)), None)
        kwargs[user_key] = kwargs[user_key].get_user_without_sensitive_data() if user_key else kwargs[user_key]
        return func(*args, **kwargs)
    return wrapper_anonymize_user


@anonymize_user
def add_vote(question_id: str, user: User, is_upvote: bool) -> None:
    """
    Vote up/down on question
    """
    try:
        db.remove_user_vote(user, question_id)
    except NotFoundError:
        # it's okay, since we always try to delete users vote before adding
        # new, even if they don't have one
        pass
    db.add_vote(user, question_id, is_upvote)


@anonymize_user
def delete_vote(question_id: str, user: User) -> None:
    """
    Delete user's vote on question
    """

    db.remove_user_vote(user, question_id)


def get_question(question_id: str, user: User) -> Question:
    """
    Gets a single question with question_id from database
    """

    question = db.get_question(question_id)
    return question.get_api_result(user)


@anonymize_user
def remove_question(question_id: str, user: User) -> None:
    """
    Remove user's given question
    """
    question = db.get_question(question_id)
    if question.author != user:
        raise UnauthorizedError("You cannot delete someone else's question.")
    if not question or len(question.votes) != 0:
        raise QuestionRemovingError
    db.remove_question(question_id)


def add_question(survey: Survey, question: str, user: User) -> ObjectId:
    """
    Add question to given survey
    """

    def check_question_requirements(question: str) -> None:
        """
        Throws error if question content doesn't
        meet requirements
        """

        if len(question) < 3:
            raise BadQuestionError("Question must have minimum 3 characters.")

    # It's enough for us to store user's host and cookie in database,
    # so to make it more anonymous, we don't save ID
    # of the question's author.
    user = user.get_user_without_sensitive_data() if survey.is_anonymous \
        else User(user.host, user.cookie, None, user.full_name, user.email)

    check_question_requirements(question)
    question_id = db.add_question(user, survey, sanitize(question), survey.is_anonymous)
    return question_id


@anonymize_user
def create_survey(title: str, hide_votes: bool, is_anonymous: bool, description: str, author: User) -> Dict[str, str]:
    """
    Create new survey
    """
    results_secret = secrets.token_hex(8)
    admin_secret = secrets.token_hex(8)
    return {
        'key': db.create_survey(sanitize(title), hide_votes, is_anonymous, results_secret,
                                admin_secret, sanitize(description), author),
        'results_secret': results_secret,
        'admin_secret': admin_secret
    }


@anonymize_user
def add_view_if_not_exists(viewer: User, survey: Survey) -> None:
    """
    Adds new view document to database if it doesn't exists yet.
    """

    db.add_view_if_not_exists(viewer, survey)


def get_all_surveys() -> List[Dict]:
    """
    Returns a list of all surveys, but with limited data about them
    (so without the questions, votes etc.).
    """

    return list(map(Survey.get_api_brief_result, db.get_all_surveys()))


@anonymize_user
def get_user_surveys(user: User) -> List[Dict]:
    """
    Returns a list of all surveys created by
    specific user with survey secret.
    """

    return list(map(Survey.get_api_brief_result_with_secrets, db.get_all_surveys(user)))


@anonymize_user
def mark_as_read(question_id: str, user: User, is_read: bool):
    """
    Mark as read
    """
    db.mark_as_read(user, question_id, is_read)
