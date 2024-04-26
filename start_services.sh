#!/bin/bash

# Start Flask server in the background
python3 app/interface/server.py &

# Wait for the Flask server to initialize
sleep 30  # Wait 30 seconds; adjust as needed for your setup

# Execute automate.py
python3 app/automate.py
