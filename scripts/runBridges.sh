#!/bin/bash
npm --prefix ./web install ./web
npm --prefix ./web build
cp web/build bridges/templates -r
cp web/build/static bridges/static -r
python3 bridges "$@"