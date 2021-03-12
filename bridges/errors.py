class BadUrlError(Exception):
    """
    This exception should be thrown when
    the user pass somewhere an url, which
    is not in correct format.
    """

    pass


class NotFoundError(Exception):
    """
    This exception should be thrown, when user
    requested a resource, which doesn't exists
    in the database.
    """

    pass


class UnauthorizedError(Exception):
    """
    This exception should be thrown, when user
    wants to do illegal stuff (like deleting not his question)
    """

    pass


class QuestionRemovingError(Exception):
    """
    This exception should be thrown, when user
    wants to remove questions, which already has
    some votes on it.
    """

    pass


class BadQuestionError(Exception):
    """
    This exception should be thrown, when question
    typed by user doesn't meet requirements.
    """

    pass


class SurveyClosedError(Exception):
    """
    This exception should be thrown when
    the user wants to perform operation
    on a survey that's not open anymore.
    """
