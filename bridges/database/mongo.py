from urllib.parse import quote_plus
import logging
from typing import List
from dacite import from_dict
from dacite.exceptions import (
    DaciteFieldError,
    ForwardReferenceError,
    MissingValueError,
    UnexpectedDataError,
    WrongTypeError,
)
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from bson.objectid import ObjectId
from bridges.errors import NotFoundError
from bridges.utils import get_url_from_title, get_url, get_url_and_number
from bridges.database.objects.vote import Vote
from bridges.database.objects.question_user_context import QuestionUserContext
from bridges.database.objects.question import Question
from bridges.database.objects.survey import Survey
from bridges.database.objects.user import User
from bridges.argument_parser import args


surveys_collection = None

MONGO_QUESTIONS_ID = 'questions._id'

QUESTION_NOT_FOUND_ERROR_MESSAGE = "Question not found."
SURVEY_NOT_FOUND_ERROR_MESSAGE = "Survey not found."

MONGO_PUSH = '$push'
MONGO_PULL = '$pull'
MONGO_SET = '$set'


def init() -> None:
    """
    Initializes a connection to mongo database
    and checks if this connection is set up properly.
    """

    global surveys_collection
    logging.info("Connecting to database %s", args.database_uri)

    client = MongoClient(host=args.database_uri,
                         username=quote_plus(args.database_user),
                         password=quote_plus(args.database_password),
                         retryWrites=False)

    try:
        client.admin.command('ismaster')
    except ConnectionFailure:
        logging.error("Could not connect to database %s", args.database_uri)
        raise

    db = client[args.database_name]
    surveys_collection = db.surveys
    logging.info("Connected to database %s", args.database_uri)


def add_vote(user: User, question_id: str, vote_type: str) -> None:
    """
    Add new vote to db
    """

    vote = Vote(user, vote_type)
    surveys_collection.update_one(
        {MONGO_QUESTIONS_ID: ObjectId(question_id)},
        {MONGO_PUSH: {'questions.$.votes': vote.as_dict()}}
    )


def create_survey(title: str, hide_votes: bool,
                  results_secret: str, admin_secret: str,
                  _: str, author: User) -> str:
    """
    Create new survey in db
    """

    encoded_uri_title = get_url_from_title(title)
    number = __get_new_survey_number(encoded_uri_title)
    survey = Survey(
        title=title,
        number=number,
        hide_votes=hide_votes,
        results_secret=results_secret,
        author=author,
        url=encoded_uri_title,
        admin_secret=admin_secret
    )
    surveys_collection.insert_one(survey.as_dict())
    return get_url(encoded_uri_title, number)


def get_question(question_id: str) -> Question:
    """
    Gets a single question from a database
    with proper question_id.
    """

    result = surveys_collection.find_one(
        {MONGO_QUESTIONS_ID: ObjectId(question_id)},
        {'questions.$': 1}
    )

    if result:
        return from_dict(data_class=Question, data=result['questions'][1])
    else:
        raise NotFoundError(QUESTION_NOT_FOUND_ERROR_MESSAGE)


def __get_new_survey_number(url: str) -> int:
    """
    Given the url of the survey (ex. 'my-url'), it gets
    from the database the surveys with the same url. If it
    has found something (ex. the survey my-url-2), it returns
    the number of this found survey increased by one (so
    in example it would return 3). If it didn't
    found any survey with this url, it returns 1.
    """

    results = surveys_collection.find({'url': url}).sort('number', -1).limit(1)
    try:
        return results.next()['number'] + 1
    except StopIteration:
        return 1


def get_survey(url: str) -> Survey:
    """
    Gets a single survey from database
    with proper url.
    """

    clear_url = '/' if url[0] == '/' else url
    url_and_number = get_url_and_number(clear_url)
    survey_db_result = surveys_collection.find_one(url_and_number)
    return from_dict(data_class=Survey,
                     data=survey_db_result) if survey_db_result else None


def set_survey_state(survey_url: str, is_open: bool) -> str:
    """
    Set survey state: whether it's open (active)
    or closed (frozen).
    """
    url_and_number = get_url_and_number(survey_url)

    result = surveys_collection.update_one(
        {'url': url_and_number['url'], 'number': url_and_number['number']},
        {MONGO_SET: {'open': is_open}})

    if result.raw_result['nModified'] == 0:
        raise NotFoundError(SURVEY_NOT_FOUND_ERROR_MESSAGE)
    return surveys_collection.find_one(url_and_number)['open']


def add_question(author: User, survey_url, content) -> ObjectId:
    """
    Add new question to db
    """

    url_and_number = get_url_and_number(survey_url)
    # We generate our own ID, so we can return it to user without asking db
    # about it
    question = Question(content=content, author=author, _id=ObjectId())
    result = surveys_collection.update_one(
        {'url': url_and_number['url'], 'number': url_and_number['number']},
        {MONGO_PUSH: {'questions': question.as_dict(skip_id=False)}})

    # We use raw_result, because MockupDB framework does not support field
    # nModified directly
    if result.raw_result['nModified'] == 0:
        raise NotFoundError(SURVEY_NOT_FOUND_ERROR_MESSAGE)
    return question._id


def add_view_if_not_exists(viewer: User, survey_url) -> None:
    """
    Adds new view document to database if it doesn't exist yet.
    """

    url_and_number = get_url_and_number(survey_url)

    previous_user_view = surveys_collection.find_one(
        {'url': url_and_number['url'], 'number': url_and_number['number'],
         'views': {'$elemMatch': viewer.get_mongo_equal_query()}}
    )

    if not previous_user_view:
        result = surveys_collection.update_one(
            {'url': url_and_number['url'], 'number': url_and_number['number']},
            {MONGO_PUSH: {'views': viewer.as_dict()}})

        if result.raw_result['nModified'] == 0:
            raise NotFoundError(SURVEY_NOT_FOUND_ERROR_MESSAGE)


def remove_question(question_id: str) -> None:
    """
    Removes the single question from the database
    with proper question_id
    """

    result = surveys_collection.update_one(
        {MONGO_QUESTIONS_ID: ObjectId(question_id)},
        {
            MONGO_PULL: {'questions': {'_id': ObjectId(question_id)}}
        })
    if result.raw_result['nModified'] == 0:
        raise NotFoundError(QUESTION_NOT_FOUND_ERROR_MESSAGE)


def remove_user_vote(user: User, question_id: str) -> None:
    """
    Remove user vote in db
    """

    result = surveys_collection.update_one(
        {MONGO_QUESTIONS_ID: ObjectId(question_id)},
        {MONGO_PULL: {
            'questions.$[elem].votes': user.get_mongo_equal_query('author')}},
        array_filters=[{'elem._id': ObjectId(question_id)}])
    if result.raw_result['nModified'] == 0:
        raise NotFoundError(QUESTION_NOT_FOUND_ERROR_MESSAGE)


def get_all_surveys(user: User = None) -> List[Survey]:
    """
    Gets all surveys from a database.
    """

    def convert_survey_without_exception(survey):
        """
        When we get all surveys from db, we don't
        want to throw exception, when something goes
        wrong in just one survey (types in that broken
        survey may be not compatible with our model,
        for example float instead of int). It's just a
        guardian, when someone modify something in db
        manually.
        """

        try:
            return from_dict(data_class=Survey, data=survey)
        except (ForwardReferenceError,
                UnexpectedDataError,
                ForwardReferenceError,
                DaciteFieldError,
                WrongTypeError,
                MissingValueError):
            return None
    surveys = map(
        convert_survey_without_exception,
        surveys_collection.find(user.get_mongo_equal_query('author')) if user
        else surveys_collection.find())
    return list(filter(None, surveys))


def mark_as_read(user: User, question_id: str, is_read: bool) -> None:
    """
    mark as read
    """

    surveys_collection.update_one(
        {MONGO_QUESTIONS_ID: ObjectId(question_id)},
        {MONGO_PULL:
         {'questions.$[elem].user_contexts':
          user.get_mongo_equal_query('author')
          }
         },
        array_filters=[{'elem._id': ObjectId(question_id)}])

    user_contexts = QuestionUserContext(user, is_read)
    surveys_collection.update_one(
        {MONGO_QUESTIONS_ID: ObjectId(question_id)},
        {MONGO_PUSH: {'questions.$.user_contexts': user_contexts.as_dict()}}
    )
