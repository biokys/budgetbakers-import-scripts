#!/bin/bash

# Create virtual environment for python3.
virtualenv -p $(which python3) env

# Install packages
source ./env/bin/activate && pip install -r requirements.txt