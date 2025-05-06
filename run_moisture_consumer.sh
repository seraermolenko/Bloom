#!/bin/zsh

source ./myenv/bin/activate

export DJANGO_SETTINGS_MODULE=bloom.settings
export PYTHONPATH=.

python kafka/consumer_moisture.py
