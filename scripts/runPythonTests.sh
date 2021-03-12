#!/bin/sh
mkdir .sonar
python3 -m pytest bridges/tests -s --disable-warnings --cov=bridges --cov-report=xml:.sonar/coverage.xml --cov-report=html:.sonar/html-coverage