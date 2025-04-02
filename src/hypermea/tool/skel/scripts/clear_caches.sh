#!/bin/bash

cd ../..
find . -type d -name __pycache__ -exec rm -rf {} \;

shopt -s dotglob
find . -type d -name .pytest_cache -exec rm -rf {} \;
shopt -u dotglob
