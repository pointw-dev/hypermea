#!/bin/bash

cd ../service
export PYTHONPATH=$(pwd)
pytest
