#!/bin/bash

# Function to check if a port is in use
check_port() {
    lsof -i :$1 >/dev/null 2>&1
    return $?
}

# Function to stop PostgreSQL service
stop_postgres() {
    echo "Stopping PostgreSQL service..."
    brew services stop postgresql@14 >/dev/null 2>&1
}

# Function to start PostgreSQL service
start_postgres() {
    echo "Starting PostgreSQL service..."
    brew services start postgresql@14 >/dev/null 2>&1
}

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Set up Python environment
export PYTHONPATH="${SCRIPT_DIR}"

if [ "$1" = "local" ]; then
    echo "Switching to local PostgreSQL configuration..."
    cp .env.local .env
    echo "Stopping Cloud SQL Proxy if running..."
    pkill -f cloud_sql_proxy >/dev/null 2>&1
    start_postgres
elif [ "$1" = "cloud" ]; then
    echo "Switching to Cloud SQL configuration..."
    cp .env.cloud .env
    
    echo "Stopping any existing Cloud SQL Proxy..."
    pkill -f cloud_sql_proxy >/dev/null 2>&1
    
    # Wait for port to be available
    echo "Waiting for port 5433 to be available..."
    while check_port 5433; do
        sleep 1
    done
    
    echo "Starting Cloud SQL Proxy on port 5433..."
    ./cloud_sql_proxy -instances=scoutmagi-soccer:us-central1:soccer-rankings-db=tcp:5433 &
    
    # Wait for proxy to start and test connection
    sleep 2
    
    # Test connection
    if ! check_port 5433; then
        echo "Error: Cloud SQL Proxy failed to start on port 5433"
        exit 1
    fi
else
    echo "Usage: ./switch_env.sh [local|cloud]"
    exit 1
fi

echo "Loading environment variables..."
source .env

echo "Environment switched successfully!"
echo "You can now run the app using either:"
echo "1. python3 app.py             (direct run)"
echo "2. python3 -m flask run       (Flask development server with auto-reload)" 