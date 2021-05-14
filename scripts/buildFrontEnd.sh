#!/bin/bash
npm --prefix ./web install ./web
npm --prefix ./web run-script build
cp -R web/build bridges/templates
cp -R web/build/static bridges/static
