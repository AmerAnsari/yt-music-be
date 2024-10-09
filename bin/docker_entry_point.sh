#!/bin/bash

# Start server
echo "Starting server"
gunicorn app:app --bind 0.0.0.0:8000 --timeout 600 --access-logfile - --error-logfile - --capture-output
