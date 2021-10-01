import logging.config
import os
from bridges.argument_parser import parse_args
parse_args()

logging_conf_path = os.path.normpath(
    os.path.join(
        os.path.dirname(__file__),
        '../logging.conf'))
logging.config.fileConfig(logging_conf_path)

# we need to parse args BEFORE importing an application,
# so application can use these args directly.
# pylint: disable=wrong-import-position, wrong-import-position
from bridges.app import main

if __name__ == "__main__":
    main()
