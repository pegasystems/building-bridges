#!/bin/bash
./scripts/buildFrontEnd.sh
python3 -m bridges "$@"