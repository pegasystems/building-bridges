from bridges.argument_parser import parse_args
parse_args(True)
from bridges.argument_parser import args


from mockupdb import MockupDB
from bridges.app import app, initialize_app


server = None
client = None


def get_client_server():
    """
    Creates a db server - mockup of mongo and
    client, that will make API calls. It also
    sets the proper settings and flags to enable
    testing.
    """

    global server
    global client

    if server and client:
        return server, client
    server = MockupDB(auto_ismaster=True)
    server.run()
    print("STARTING TEST DB AT", server.uri)
    app.testing = True
    args.contact_email = "email@example.com"
    args.database_uri = server.uri
    initialize_app(app)
    client = app.test_client()
    return server, client
