#!/bin/bash
npm --prefix ./web install ./web
npm --prefix ./web run-script build
cp web/build bridges/templates -r
cp web/build/static bridges/static -r