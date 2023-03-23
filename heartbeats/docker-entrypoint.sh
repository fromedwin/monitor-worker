#!/bin/bash
pip3 install -r /etc/monitor-worker/requirements.txt

# Start heartbeats to ping backend every xxx seconds
python3 /etc/monitor-worker/scripts/heartbeats.py &

# Start python APIs
cd /etc/monitor-worker/heartbeats/

# DEV
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
# PROD
# uvicorn main:app --host 0.0.0.0 --port 8000