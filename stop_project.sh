#!/bin/zsh

echo "Stopping all project processes..."

pkill -f kafka.Kafka
pkill -f daphne
pkill -f consumer_moisture.py
pkill -f npm

echo "All processes stopped."
