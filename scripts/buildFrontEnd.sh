#!/bin/bash
npm --prefix ./web install ./web
npm --prefix ./web run-script build
rm -f bridges/templates -r
rm -f bridges/static -r
cp -R web/build bridges/templates
cp -R web/build/static bridges/static
