from dataclasses import asdict
from typing import Dict


class MongoObject(object):
    """
    Default parent for any mongo object.
    """

    def as_dict(self, skip_id=True) -> Dict:
        """
        There is no functionality in asdict function from
        dataclasses to skip some variable, so we do this
        little hack instead to ignore the '_id' variable.
        """

        d = asdict(self)
        if skip_id:
            d.pop('_id', None)
        return d
