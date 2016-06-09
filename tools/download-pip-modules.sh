#!/bin/bash

mkdir -p pip

pip install --target=pip bottle
pip install --target=pip configparser
pip install --target=pip daemonize
pip install --target=pip schedule
