
#!/bin/bash

# Ensure the API key is set.
if [ -z "$SANCTUM_API_KEY" ]; then
  echo "?? Error: SANCTUM_API_KEY environment variable is not set."
  echo "? Please set it before running this script:"
  echo "export SANCTUM_API_KEY='your-secret-key-here'"
  exit 1
fi

echo "? Starting Covenant Memory Engine (CME) Service on port 8000..."
uvicorn src.cme_service:app --host 0.0.0.0 --port 8000 &
CME_PID=$!

echo "? Starting Pivot Analyzer Service on port 8001..."
uvicorn src.pivot_service:app --host 0.0.0.0 --port 8001 &
PIVOT_PID=$!

# Wait a couple of seconds for services to start
sleep 2

# Check if ngrok is installed
if ! command -v ngrok &> /dev/null
then
    echo "?? ngrok could not be found. Please install it from https://ngrok.com/download"
    kill $CME_PID
    kill $PIVOT_PID
    exit 1
fi


echo "? Starting ngrok tunnels..."
# The ngrok dashboard is available at http://127.0.0.1:4040
ngrok http 8000 --log=stdout > ngrok_cme.log &
ngrok http 8001 --log=stdout > ngrok_pivot.log &

# Function to clean up background processes
cleanup() {
    echo "\n? Shutting down services and ngrok..."
    kill $CME_PID
    kill $PIVOT_PID
    # Kill all ngrok processes
    killall ngrok
    echo "? Done."
}

# Trap SIGINT (Ctrl+C) and call cleanup
trap cleanup SIGINT

echo "?? Services are running. Press Ctrl+C to stop."
echo "   - CME Service on http://localhost:8000"
echo "   - Pivot Service on http://localhost:8001"
echo "   - ngrok dashboard on http://localhost:4040"
echo "?? Check ngrok_cme.log and ngrok_pivot.log for public URLs."

# Wait for all background processes to finish
wait
