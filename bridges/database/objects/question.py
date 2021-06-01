from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass, field
from bson.objectid import ObjectId
from bridges.database.objects.question_user_context import QuestionUserContext
from .vote import Vote
from .user import User
from .mongo_object import MongoObject


@dataclass
class Question(MongoObject):
    """
    Template of question
    """

    content: str
    author: User
    hidden: Optional[bool] = False
    votes: List[Vote] = field(default_factory=list)
    user_contexts: List[QuestionUserContext] = field(default_factory=list)
    _id: ObjectId = None
    date: datetime = field(default_factory=datetime.now)

    def get_api_result(self, user: User, hide_votes=False):
        upvotes = sum(1 if vote.upvote else 0 for vote in self.votes)
        downvotes = len(self.votes) - upvotes
        voted = self.get_user_vote(user)
        is_read = self.is_read(user)
        return {
            **self.as_dict(skip_id=False),
            ** {
                "upvotes": upvotes if not hide_votes or voted != 'none' or is_read == 'true' else None,
                "downvotes": downvotes if not hide_votes or voted != 'none' or is_read == 'true' else None,
                "voted": voted,
                "read": is_read,
                "isAuthor": self.author == user
            }
        }

    def is_read(self, user: User):
        if any(ctx.read == 'true' and ctx.author == user for ctx in self.user_contexts):
            return "true"
        else:
            return "false"

    def get_user_vote(self, user: User):
        """
        How user voted on question
        """

        if any(v.upvote and v.author == user for v in self.votes):
            return 'up'
        elif any(not v.upvote and v.author == user for v in self.votes):
            return 'down'
        else:
            return 'none'
