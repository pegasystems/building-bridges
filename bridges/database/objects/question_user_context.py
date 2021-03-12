from dataclasses import dataclass
from .mongo_object import MongoObject
from .user import User


@dataclass
class QuestionUserContext(MongoObject):
    """
    Template of vote
    """

    author: User
    read: str
