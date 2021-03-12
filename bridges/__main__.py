from bridges.argument_parser import parse_args
parse_args()

# we need to parse args BEFORE importing an application,
# so application can use these args directly.
# pylint: disable=wrong-import-position, wrong-import-position
from bridges.app import main

if __name__ == "__main__":
    main()
