from urllib.parse import urlparse
from typing import Dict
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.constants import OneLogin_Saml2_Constants
from flask import session, request, redirect, Flask
from bridges.argument_parser import args


ASSERTION_CUSTOMER_SERVICE = '/oauth2/callback/saml/'


def load(app: Flask) -> None:
    """
    Main function to load SAML plugin. It'll
    create a proper endpoint and after user is
    authenticated by the IdP, it'll set a samlNameId
    in a session storage.
    """

    # pylint: disable=unused-variable
    @app.route(ASSERTION_CUSTOMER_SERVICE, methods=['POST'])
    def accept_login():
        """
        Assertion customer service, IdP should call this endpoint
        with user identification.
        """

        request_id = None
        if 'AuthNRequestID' in session:
            request_id = session['AuthNRequestID']

        auth = get_auth()
        auth.process_response(request_id=request_id)
        errors = auth.get_errors()
        if len(errors) == 0:
            if 'AuthNRequestID' in session:
                del session['AuthNRequestID']
            session['samlNameId'] = auth.get_nameid()
            return redirect(auth.redirect_to(request.form['RelayState']))
        else:
            print(auth.get_last_error_reason())
            return "Saml authentication failed!"

    # pylint: disable=unused-variable
    @app.before_request
    def redirect_to_login_page_if_needed():
        """
        Before each request, we check if requester is authenticated -
        if not, we redirect him/her to the IdP
        """

        if not is_user_authenticated() and request.path != ASSERTION_CUSTOMER_SERVICE:
            return redirect(get_auth().login())

        return None

    def init_saml_auth(req: Dict):
        """
        Configuration function for SAML library
        """

        auth = OneLogin_Saml2_Auth(req, {
            "strict": True,
            # Debug just print in console, so we can leave that in production
            "debug": True,
            "sp": {
                "entityId": args.saml_entity_id,
                "assertionConsumerService": {
                    "url": f"{args.saml_domain}{ASSERTION_CUSTOMER_SERVICE}",
                    "binding": OneLogin_Saml2_Constants.BINDING_HTTP_POST
                },
                "NameIDFormat": OneLogin_Saml2_Constants.NAMEID_UNSPECIFIED
            },
            "idp": {
                "entityId": args.saml_provider_id,
                "singleSignOnService": {
                    "url": args.saml_login_url,
                    "binding": OneLogin_Saml2_Constants.BINDING_HTTP_REDIRECT
                },
                "x509cert": args.saml_cert
            }
        })
        return auth

    def is_user_authenticated():
        """
        Returns true if user is already authenticated
        by the IdP Server.
        """

        return 'samlNameId' in session

    def prepare_flask_request(req) -> Dict:
        """
        Returns dictionary with information
        about request needed for SAML library.
        """

        url_data = urlparse(req.url)
        return {
            'https': 'on' if req.scheme == 'https' else 'off',
            'http_host': req.host,
            'server_port': url_data.port,
            'script_name': req.path,
            'get_data': req.args.copy(),
            'post_data': req.form.copy()
        }

    def get_auth():
        """
        Returns auth object needed for SAML library.
        """
        req = prepare_flask_request(request)
        return init_saml_auth(req)
