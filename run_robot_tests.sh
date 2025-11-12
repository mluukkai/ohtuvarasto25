#!/bin/bash
# Script to run Robot Framework E2E tests

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Start Flask application in background
cd "$SCRIPT_DIR/src"
export FLASK_DEBUG=false
poetry run python app.py &
FLASK_PID=$!

# Wait for application to start
echo "Waiting for Flask to start..."
sleep 5

# Run Robot Framework tests
cd "$SCRIPT_DIR"
poetry run robot --outputdir robot-results src/tests/robot/varasto_web.robot

# Store exit code
TEST_EXIT_CODE=$?

# Kill Flask application
kill $FLASK_PID 2>/dev/null || true

# Exit with test result
exit $TEST_EXIT_CODE
