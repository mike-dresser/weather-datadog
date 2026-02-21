#!/bin/bash
# Script to run the Weather to Datadog Metrics Service

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Path to the secrets file
SECRETS_FILE="${SCRIPT_DIR}/.env"

# Check if secrets file exists
if [ ! -f "$SECRETS_FILE" ]; then
    echo "Error: Secrets file not found at $SECRETS_FILE"
    echo "Please create a .env file based on .env.example"
    exit 1
fi

# Load environment variables from secrets file
set -a
source "$SECRETS_FILE"
set +a

# Validate that all required variables are set
if [ -z "$OPENWEATHER_API_KEY" ] || [ "$OPENWEATHER_API_KEY" = "your_openweather_api_key_here" ]; then
    echo "Error: OPENWEATHER_API_KEY is not set or is using the default value"
    exit 1
fi

if [ -z "$DATADOG_API_KEY" ] || [ "$DATADOG_API_KEY" = "your_datadog_api_key_here" ]; then
    echo "Error: DATADOG_API_KEY is not set or is using the default value"
    exit 1
fi

if [ -z "$DATADOG_APP_KEY" ] || [ "$DATADOG_APP_KEY" = "your_datadog_app_key_here" ]; then
    echo "Error: DATADOG_APP_KEY is not set or is using the default value"
    exit 1
fi

if [ -z "$ZIP_CODE" ] || [ "$ZIP_CODE" = "10001" ]; then
    echo "Warning: ZIP_CODE is not set or is using the default value"
fi

# Change to script directory
cd "$SCRIPT_DIR"

# Path to virtual environment
VENV_DIR="${SCRIPT_DIR}/venv"

# Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Error: Virtual environment not found at $VENV_DIR"
    echo "Please create it first with: python3 -m venv venv"
    echo "Then install dependencies with: source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source "${VENV_DIR}/bin/activate"

# Verify virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Error: Failed to activate virtual environment"
    exit 1
fi

# Run the Python application
python weather_datadog.py
