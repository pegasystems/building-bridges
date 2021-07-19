
import logging.config

import re
import os, socket
from flask import Flask, Blueprint, render_template, request, session, g
from bridges.api.endpoints.surveys import ns as surveys_namespace
from bridges.api.endpoints.questions import ns as questions_namespace
from bridges.api.endpoints.votes import ns as votes_namespace
from bridges.api.endpoints.user_contexts import ns as question_user_contexts_namespace
from bridges.api.endpoints.info import ns as info_namespace
from bridges.database.mongo import init as mongo_init
from bridges.api.restplus import api
from bridges.argument_parser import args
from bridges.utils import get_user_name_and_email_from_session
from werkzeug.contrib.fixers import ProxyFix
from bridges.database.objects.user import User
import secrets
import bridges.auth.saml.saml
import hashlib

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = False


# Cookie name in the users browser
CLIENT_ID_COOKIE = "CLIENT_ID"

# Every new namespace should go here
NAMESPACES = [surveys_namespace,
              questions_namespace,
              votes_namespace,
              question_user_contexts_namespace,
              info_namespace]

app = Flask(__name__)

# In order to use session in flask we need to
# set the secret key to encrypt cookies
app.config['SECRET_KEY'] = os.urandom(16)

# Swagger has problems with proxy, so we need to add this magic line to
# make it work with k8s service
app.wsgi_app = ProxyFix(app.wsgi_app)

logging_conf_path = os.path.normpath(
    os.path.join(
        os.path.dirname(__file__),
        '../logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)


def configure_app(flask_app: Flask) -> None:
    """
    Here we set some flask options.
    """

    if not args.debug:
        flask_app.config['ENV'] = ""
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = RESTPLUS_ERROR_404_HELP


def add_namespaces() -> None:
    """
    We add all namespaces to api points here. After you
    create a new namespace, you should add it in proper variable.
    """

    for namespace in NAMESPACES:
        api.add_namespace(namespace)


def initialize_app(flask_app: Flask) -> None:
    """
    We set up a Flask app and add all namespaces to it,
    and initialize mongo connection here.
    """

    configure_app(flask_app)
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    add_namespaces()
    if args.enable_saml:
        bridges.auth.saml.saml.load(flask_app)
    flask_app.register_blueprint(blueprint)
    mongo_init()


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    """
    Since we don't use any templating language,
    we just return a file with proper javascript,
    that will generate the website.
    """

    return render_template("index.html")


@app.before_request
def get_user():
    """
    This functions set the 'User' attribute (which is based
    on IP of client, cookie value and user id) to a request variable,
    so later program can use these easily.
    """

    def get_host_from_request():
        """
        If building bridges is behind proxy, the proper
        client ip should be in some header. If it's not there,
        we just get the IP address of request, and we try to use
        reverse dns (and we hope, that this reverse dns domain won't change
        after user changed his IP address). If we couldn't get the domain,
        we just return ip address.
        """

        ip = request.headers.get(args.real_ip_header) or request.remote_addr
        name, _, _ = socket.gethostbyaddr(ip)
        return name or ip

    def get_cookie_from_request():
        """
        We try to get a cookie from client. If it's not there -
        we create a new one.
        """

        cookie = request.cookies.get(CLIENT_ID_COOKIE)
        if not cookie:
            cookie = secrets.token_hex(16)
        return cookie

    def get_hashed_id_from_session():
        """
        If SAML is enabled, user ID should be saved in samlNameId.
        We will return hashed ID using SHA256, so we don't have plaintext
        users in database.
        """

        user_id = session.get('samlNameId')
        return hashlib.sha256(str.encode(user_id)).hexdigest() if user_id else None

    user_data = get_user_name_and_email_from_session()
    user = User(get_host_from_request(), get_cookie_from_request(), get_hashed_id_from_session(),
                user_data['userFullName'], user_data['userEmail'])
    request.user = user


@app.after_request
def set_cookie(response):
    """
    After the request, we set the cookie to the client's browser.
    """
    try:
        response.set_cookie(CLIENT_ID_COOKIE, request.user.cookie, max_age=60*60*24*365*10)
    except AttributeError:
        # When users are accessing SSO server to authorize, we may not have an information
        # about them yet.
        pass
    return response


def main():
    """
    Opening function for the program.
    """

    initialize_app(app)
    print("*********************")
    log.info(
        '>>>>> Starting server at http://0.0.0.0:%d/api/ <<<<<' % args.port)
    app.run(debug=args.debug, port=args.port, host="0.0.0.0")
