from bridges.argument_parser import parse_args
parse_args(True)

# DO NOT delete app from import - it may seem it's unused, but it's used by gunicorn
from bridges.app import main, app
main(True)
