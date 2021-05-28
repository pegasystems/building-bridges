import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
from bson.objectid import ObjectId
from bridges.utils import get_url
from bridges.database.objects.mongo_object import MongoObject
from .question import Question
from .user import User


@dataclass
class Survey(MongoObject):
    """
    Template of survey
    """

    title: str
    number: int
    author: User
    results_secret: Optional[str]
    admin_secret: Optional[str]
    _id: ObjectId = None
    hide_votes: Optional[bool] = False
    open: Optional[bool] = True
    url: Optional[str] = None
    description = None
    questions: List[Question] = field(default_factory=list)
    date: datetime = field(default_factory=datetime.now)
    views: List[User] = field(default_factory=list)

    @property
    def key(self):
        """
        Returns a url combined with the number of the survey
        """

        return get_url(self.url, self.number)

    def get_api_result(self, user: User, user_results_secret: str, user_admin_secret: str) -> Dict:
        """
        Creates an api result from the database object (itself),
        so we don't expose the author of the question and details
        about votes, but just needed information.
        """

        result = self.as_dict()
        result['questions'] = []

        result["key"] = self.key
        result["hideVotes"] = self.hide_votes
        result["viewsNumber"] = self._count_views()
        result["votersNumber"] = self._count_voters()
        result["questionersNumber"] = self._count_questioners()
        for question in filter(lambda q: not q.hidden or self.admin_secret == user_admin_secret, self.questions):
            hide_votes = self.open and self.hide_votes and self.results_secret != user_results_secret and self.admin_secret != user_admin_secret
            result['questions'].append(question.get_api_result(user, hide_votes))
        return result

    @staticmethod
    def unique_users(users_list) -> [User]:
        return list(set(users_list))

    def _count_views(self) -> int:
        return len(self.unique_users(self.views))

    def _count_questioners(self) -> int:
        all_questioners = list(map(lambda q: q.author, self.questions))
        unique_questioners = self.unique_users(all_questioners)
        return len(unique_questioners)

    def _count_voters(self) -> int:
        all_votes = list(map(lambda q: q.votes, self.questions))
        all_votes_flattened = [v for sublist in all_votes for v in sublist]
        all_voters = list(map(lambda q: q.author, all_votes_flattened))
        unique_voters = self.unique_users(all_voters)
        return len(unique_voters)

    def get_api_brief_result(self) -> Dict:
        """
        Creates an api result from the database object (itself),
        with just a few fields. This function is used to get list of
        all surveys, with brief information.
        """

        result = {}
        result['title'] = self.title
        result['key'] = self.key
        result['date'] = self.date
        result['hideVotes'] = self.hide_votes
        result['viewsNumber'] = self._count_views()
        result['votersNumber'] = self._count_voters()
        result['questionersNumber'] = self._count_questioners()
        return result

    def get_api_brief_result_with_secrets(self) -> Dict:
        """
        Creates an api result, same as in get_api_brief_result function,
        but with survey secrets.
        """

        result = self.get_api_brief_result()
        result['results_secret'] = self.results_secret
        result['admin_secret'] = self.admin_secret
        return result
