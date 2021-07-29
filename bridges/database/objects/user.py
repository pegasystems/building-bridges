from dataclasses import dataclass
from typing import Optional
from .mongo_object import MongoObject


@dataclass(frozen=True)
class User(MongoObject):
    """
    Template of user
    """
    host: str
    cookie: Optional[str]
    user_id: Optional[str]
    full_name: Optional[str]
    email: Optional[str]

    def __hash__(self):
        return hash(self.user_id)

    def __eq__(self, other):
        if other.__class__ is not self.__class__:
            return False

        if self.user_id and other.user_id:
            return self.user_id == other.user_id

        return self.host == other.host or self.cookie == other.cookie

    def get_mongo_equal_query(self, prefix=''):
        prefix = prefix + '.' if prefix != '' else prefix
        return {
            "$or": [
                {
                    "$and": [
                        {f'{prefix}user_id': None},
                        {"$or": [
                            {f'{prefix}host': self.host},
                            {f'{prefix}cookie': self.cookie}
                        ]}
                    ],
                },
                {f'{prefix}user_id': self.user_id if self.user_id else ''}
            ]
        }

    def get_user_without_sensitive_data(self, clear_user_id=False):
        user_id = None if clear_user_id else self.user_id
        return User(self.host, self.cookie, user_id, None, None)
