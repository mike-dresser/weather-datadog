# Weather to Datadog Metrics Service

A Python application that retrieves current temperature and humidity from the OpenWeather API for a given ZIP code and submits them as custom metrics to Datadog.

## Features

- Fetches weather data from OpenWeather API
- Submits custom gauge metrics to Datadog:
  - `environment.temperature.outside` (in Fahrenheit)
  - `environment.humidity.outside` (percentage)
- Logs all operations to stdout
- Runs continuously, checking every 15 seconds
- Graceful shutdown on SIGINT/SIGTERM

## Requirements

- Python 3.6+
- OpenWeather API key
- Datadog API key and Application key

## Setup

### 1. Create a Virtual Environment (Recommended)

Create and activate a virtual environment to isolate dependencies:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate
```

When activated, your terminal prompt will show `(venv)` at the beginning.

To deactivate the virtual environment later:
```bash
deactivate
```

### 2. Install Dependencies

With the virtual environment activated, install the required packages:

```bash
pip install -r requirements.txt
```

## Configuration

1. Copy the example secrets file:
```bash
cp .env.example .env
```

2. Edit `.env` and set the following values:

- `OPENWEATHER_API_KEY`: Your OpenWeather API key
- `DATADOG_API_KEY`: Your Datadog API key
- `DATADOG_APP_KEY`: Your Datadog Application key
- `ZIP_CODE`: The US ZIP code to monitor (e.g., "10001")

**Note:** The `.env` file contains sensitive credentials and is excluded from version control via `.gitignore`.

## Usage

Simply run the provided script:

```bash
./run.sh
```

The script will:
- Load environment variables from `.env`
- Validate that all required variables are set
- Run the Python application

Alternatively, you can run the Python script directly after setting environment variables manually:

```bash
export OPENWEATHER_API_KEY="your_openweather_api_key"
export DATADOG_API_KEY="your_datadog_api_key"
export DATADOG_APP_KEY="your_datadog_app_key"
export ZIP_CODE="10001"

python weather_datadog.py
```

The application will run continuously, fetching weather data and submitting metrics every 15 seconds. Press `Ctrl+C` to stop gracefully.

## Example Output

```
2026-02-21 10:30:00 - INFO - Datadog initialized successfully
2026-02-21 10:30:00 - INFO - Starting weather monitoring service...
2026-02-21 10:30:00 - INFO - Monitoring ZIP code: 10001
2026-02-21 10:30:00 - INFO - Press Ctrl+C to stop
2026-02-21 10:30:00 - INFO - Fetching weather data for ZIP code: 10001
2026-02-21 10:30:01 - INFO - Received weather data - Temperature: 45.2°F, Humidity: 65%
2026-02-21 10:30:01 - INFO - Submitted metric: environment.temperature.outside = 45.2°F
2026-02-21 10:30:01 - INFO - Submitted metric: environment.humidity.outside = 65%
2026-02-21 10:30:01 - INFO - Waiting 15 seconds until next check...
```
