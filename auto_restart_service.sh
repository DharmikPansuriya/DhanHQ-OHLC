#!/bin/bash

# Define the endpoint URL
ENDPOINT="http://localhost:5005/api/v1/health"

# Define the interval in seconds (e.g., 10 seconds)
INTERVAL=10

if [ -f .env ]; then
    export $(cat .env | xargs)
fi

echo "Environment: ${ENVIRONMENT}"

# CPU usage threshold
THRESHOLD=75

# Define the commands to install, build, and restart the server
INSTALL_COMMAND="sudo apt install sysstat"

RESTART_COMMAND=""

if [ "$ENVIRONMENT" == "production" ]; then
    RESTART_COMMAND="docker compose -f production.yml up --build -d"
elif [ "$ENVIRONMENT" == "development" ]; then
    RESTART_COMMAND="docker compose -f development.yml up --build -d"
fi

# Install the required packages and build docker containers
$INSTALL_COMMAND
$RESTART_COMMAND

sleep $INTERVAL
sleep $INTERVAL

# Loop indefinitely
while true; do
    # Get the current CPU usage
    CPU_USAGE=$(mpstat 1 1 | awk '/Average:/ {print 100 - $12}')
    echo "Info: Current CPU Usage at ${CPU_USAGE}%"

    # Check if the current usage exceeds the threshold
    if (( $(echo "$CPU_USAGE > $THRESHOLD" | bc -l) )); then
        echo "Warning: High CPU usage at ${CPU_USAGE}%"

        # Kill the server and restart
        echo "Killing server and restarting..."
        docker kill analytics_backend_production
        $RESTART_COMMAND
    fi

    # Use curl to send a request to the endpoint
    RESPONSE=$(curl --silent --output /dev/null --write-out "%{http_code}" "$ENDPOINT")


    # Check if the response is OK (HTTP 200)
    if [ "$RESPONSE" -eq 200 ]; then
        date "+%H:%M:%S Response OK. Doing nothing."
    else
        date "+%H:%M:%S Response not OK. Firing a command."

        # Restart the server
        $RESTART_COMMAND
        sleep $INTERVAL
        sleep $INTERVAL
    fi

    # Wait for the specified interval before next check
    sleep $INTERVAL
done
