#!/bin/bash

checkbashisms *.sh

flake8 --ignore E501 *.py
pylint --disable C0301 *.py
pyflakes *.py
mypy *.py
