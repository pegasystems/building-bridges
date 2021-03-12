import logging

from typing import Dict, Tuple
from http import HTTPStatus
from flask_restx import Resource
from bridges.argument_parser import args
from bridges.api.restplus import api


log = logging.getLogger(__name__)

ns = api.namespace('info', description='Generic api calls')


@ns.route('/email')
class ContactEmail(Resource):
    """
    Api points to operate on contact
    email.
    """

    @classmethod
    def get(cls) -> Tuple[Dict, int]:
        """
        Return contact email
        """
        return args.contact_email, HTTPStatus.OK
