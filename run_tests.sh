#!/bin/bash

# Load test environment variables
export $(grep -v '^#' .env.test | xargs)

# Start the main API server in background
PYTHONPATH=/home/shaurya/Desktop python -m gfg.backend.test_main &
SERVER_PID=$!
sleep 2  # Wait for server to start

# Run tests from project root
echo "Running API tests..."
PYTHONPATH=/home/shaurya/Desktop python -m pytest tests/test_api.py -v
TEST_RESULT=$?

# Stop the server
kill $SERVER_PID

# Exit with test result status
exit $TEST_RESULT
