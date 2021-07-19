import re
from bridges.errors import BadUrlError
from typing import Dict
from flask import session


def get_url(title: str, number: int) -> str:
    """
    Returns title of the survey combined with the number
    of survey.

    >>> get_url("title", 123)
    title-123
    """

    return title + '-' + str(number)


def get_url_from_title(title: str) -> str:
    """
    Returns encoded URI title from a string.

    >>> get_url_from_title("title$t!s")
    title-t-s
    """

    return re.sub(r'[^a-zA-Z-_]', "-", title).lower()


def get_url_and_number(url: str) -> Dict[str, str]:
    """
    Returns a splitted url to a title and the number.

    >>> get_url_and_number("title-2")
    {
        'url': title
        'number': 2
    }
    """

    last_dash_character = url.rfind('-')
    if last_dash_character == -1:
        raise BadUrlError("Couldn't get the index of the survey")
    try:
        return {
            'url': url[0:last_dash_character],
            'number': int(url[last_dash_character + 1:])
        }
    except (IndexError, ValueError):
        raise BadUrlError("Couldn't get the index of the survey")


def get_user_name_and_email_from_session():
    """
    If SAML is enabled, user full name and email should be saved in samlFullName and samlEmail.
    """

    user_full_name = session.get('samlFullName')
    user_email = session.get('samlEmail')
    return {
        'userFullName': user_full_name,
        'userEmail': user_email
    }


def dict_subset(dictionary: Dict, keys: set) -> Dict:
    """
    Returns a dictionary with restricted keys, which are
    from the other set.

    >>> dict_subset({"key1": "value1", "key2": "value2"}, {"key1"})
    {"key1": "value1"}
    """

    return {key: value for key, value in dictionary.items() if key in keys}


def sanitize(string: str, max_lines=20, max_length=2000) -> str:
    """
    This function just limits the string length and string 'heightness' -
    html sanitizing is not needed here. It additionally strip the string.

    >>> sanitize("very very very very long string", max_length = 4)
    "very"

    >>> sanitize("string \n with \n multiple \n lines", max_lines = 2)
    "string \n with"
    """

    if not string:
        return string

    limited_lines_string = "\n".join(string.split("\n")[:max_lines])
    return limited_lines_string[:max_length].strip()
