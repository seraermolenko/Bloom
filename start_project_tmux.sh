#!/bin/zsh

SESSION="bloom"

tmux kill-session -t $SESSION 2>/dev/null

# Kafka
tmux new-session -d -s $SESSION -n server 'kafka-server-start /opt/homebrew/etc/kafka/kraft/server.properties'

# Daphne (backend)
tmux split-window -v -t $SESSION 'source myenv/bin/activate && daphne bloom.asgi:application'

# Kafka moisture consumer
tmux split-window -v -t $SESSION 'source myenv/bin/activate && PYTHONPATH=. DJANGO_SETTINGS_MODULE=bloom.settings python kafka/consumer_moisture.py'

# React frontend
tmux new-window -t $SESSION -n frontend 'cd bloom-frontend && npm run dev'

tmux select-window -t $SESSION:0
tmux attach-session -t $SESSION
