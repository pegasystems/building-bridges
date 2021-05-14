#!/bin/bash
npm --prefix ./web install ./web
npm --prefix ./web run-script build
rm -r bridges/static/
rm -r bridges/templates/
cp -R web/build bridges/templates
cp -R web/build/static bridges/static
