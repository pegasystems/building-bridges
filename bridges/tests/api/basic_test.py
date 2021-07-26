import unittest
import json

from datetime import datetime
from bson.objectid import ObjectId
from mockupdb import go

from bridges.tests.api.utils import get_client_server

API_NAMESPACE = "api/"
APP_JSON_CONTENT_TYPE = 'application/json'
ADMIN_SECRET = 's3cr3t'
USER = {
    'host': 'host1.example.com',
    'cookie': 'cookie1',
    'user_id': 'abcdefghijklmnop'
}


class BasicTest(unittest.TestCase):

    @staticmethod
    def get_survey(is_open=True):
        return {
            '_id': ObjectId('666f6f2d6261722d71757578'),
            'title': 'title',
            'number': 1,
            'results_secret': 'secret',
            'admin_secret': ADMIN_SECRET,
            'author': USER,
            'open': is_open
        }

    def mock_get_info_about_survey(self, is_open=True):
        request = self.server.receives()
        request.ok(cursor={
            'id': 1,
            'firstBatch': [
                self.get_survey(is_open)
            ]
        })

    @classmethod
    def setUpClass(cls):
        cls.server, cls.client = get_client_server()

        # We generate 100 example ids for our tests
        cls.example_ids = [ObjectId() for _ in range(0, 100)]

    def make_future_get_request(self, url: str, data = None):
        url = API_NAMESPACE + url
        if data:
            return go(self.client.get, url, data=data, content_type=APP_JSON_CONTENT_TYPE)
        else:
            return go(self.client.get, url)

    def make_future_post_request(self, url: str, data: dict):
        return go(self.client.post, API_NAMESPACE + url, data=json.dumps(data),
                  content_type=APP_JSON_CONTENT_TYPE)

    def make_future_delete_request(self, url: str):
        return go(self.client.delete, API_NAMESPACE + url)

    def make_future_put_request(self, url: str = '', data: dict = None):
        return go(self.client.put, API_NAMESPACE + url, data=json.dumps(data),
                  content_type=APP_JSON_CONTENT_TYPE)

    def sample_timestamp(self) -> datetime:
        return datetime(2020, 7, 7, 14, 26, 38, 47000)

    def sample_timestamp_string(self):
        return self.sample_timestamp().isoformat()

