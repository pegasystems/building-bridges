#!/bin/sh
npm --prefix ./web install ./web
npm --prefix ./web run jest ./web -- --coverage