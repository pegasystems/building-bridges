import argparse
import configargparse
import os
from dotenv import load_dotenv


# Load environment variables from '.env' file
load_dotenv()


parser = configargparse.ArgumentParser(description='Building bridges')

# App arguments
parser.add_argument(
    '--secretkey',
    type=str,
    default=os.urandom(16),
    dest='session_secret_key',
    env_var="SECRET_KEY",
    help='Flask session secret key'
)

# Database arguments
parser.add_argument(
    '-d',
    '--dburi',
    type=str,
    default="mongodb://localhost:27017",
    dest='database_uri',
    env_var="DB_URI",
    help='Uri of mongo db instance (e.g. mongodb://localhost:27017)')
parser.add_argument(
    '--dbuser',
    type=str,
    default="",
    dest='database_user',
    env_var="DB_USER",
    help='User name for authentication in mongo db instance')
parser.add_argument(
    '--dbpassword',
    type=str,
    default="",
    dest='database_password',
    env_var="DB_PASSWORD",
    help='Password for authentication in mongo db instance')
parser.add_argument(
    '--dbname',
    type=str,
    default="building-bridges",
    dest='database_name',
    env_var="DB_NAME",
    help='Name of the mongo database (e.g. building-bridges)')


# Application arguments
parser.add_argument(
    '-p',
    '--port',
    type=int,
    default=8888,
    env_var="APP_PORT",
    help='Port number of the building-bridges API service (e.g 8888)')
parser.add_argument(
    '--debug',
    action="store_true",
    default=False,
    env_var="FLASK_DEBUG",
    help='Flask debug (dont use on production!)')
parser.add_argument(
    '--realipheader',
    type=str,
    default="x-real-ip",
    dest='real_ip_header',
    env_var="REAL_IP_HEADER",
    help='If building bridges is behind reverse proxy, ' +
        'the proper client ip should be in this header'
)


# SAML arguments
parser.add_argument(
    '--enablesaml',
    action="store_true",
    dest='enable_saml',
    default=False,
    env_var="SAML_ENABLED",
    help='Enable saml authentication'
)
parser.add_argument(
    '--samldomain',
    type=str,
    dest='saml_domain',
    env_var="SAML_DOMAIN",
    help='Domain on which the building bridges is hosted (e.g. https://example.com)'
)
parser.add_argument(
    '--samlentityid',
    type=str,
    dest='saml_entity_id',
    env_var="SAML_ENTITY_ID",
    help='ID of the application in a SAML provider (e.g. https://example.com)'
)
parser.add_argument(
    '--samlproviderid',
    type=str,
    dest='saml_provider_id',
    env_var="SAML_PROVIDER_ID",
    help='ID of the IdP (e.g. https://sts.windows.net/1a2b3c-4d5e-6f7g8h-9i/'
)
parser.add_argument(
    '--samlloginurl',
    type=str,
    dest='saml_login_url',
    env_var="SAML_LOGIN_URL",
    help='Login url of the IdP (e.g. https://login.microsoftonline.com/1a2b3c-4d5e-6f7g8h-9i/saml2'
)
parser.add_argument(
    '--samlcert',
    type=str,
    dest='saml_cert',
    env_var="SAML_CERT",
    help='Certificate of the IdP (e.g. MIIC8DCCAdig...)'
)
parser.add_argument(
    '--contactemail',
    type=str,
    default="",
    dest='contact_email',
    env_var="CONTACT_EMAIL",
    help='Contact email to show at the footer (e.g. admin@example.com)'
)

# args is not a constant here, it's modified by
# parse_args function by 'global' syntax
# pylint: disable=invalid-name
args = None

def parse_args(ignore_unused=False) -> None:
    """
    Parse arguments from the console
    and save them in the settings.
    """
    # args is not a constant, and we need global args,
    # so all files can use these args
    # pylint: disable=invalid-name, global-statement
    global args
    if ignore_unused:
        args, _ = parser.parse_known_args()
    else:
        args = parser.parse_args()