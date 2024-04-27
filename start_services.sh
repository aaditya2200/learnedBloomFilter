#!/bin/bash

# Start Flask server in the background
python3 app/interface/server.py

# Wait for the Flask server to initialize
sleep 10  # Wait 10 seconds; adjust as needed for your setup

echo "Starting Automation..."

# Execute automate.py
python3 app/automate.py
