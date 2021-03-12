from datetime import datetime
from dataclasses import dataclass, field
from .mongo_object import MongoObject
from .user import User


@dataclass
class Vote(MongoObject):
    """
    Template of vote
    """

    author: User
    upvote: bool
    date: datetime = field(default_factory=lambda: datetime.now())
