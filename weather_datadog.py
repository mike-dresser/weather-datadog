#!/usr/bin/env python3
"""
Weather to Datadog Metrics Service

Retrieves temperature and humidity from OpenWeather API for a given ZIP code
and submits them as custom metrics to Datadog.
"""

import os
import sys
import time
import logging
import signal
from typing import Optional
import requests
from datadog import initialize, api

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Global flag for graceful shutdown
shutdown_flag = False


def signal_handler(signum, frame):
    """Handle shutdown signals gracefully."""
    global shutdown_flag
    logger.info("Received shutdown signal, stopping...")
    shutdown_flag = True


def get_weather_data(zip_code: str, api_key: str) -> Optional[dict]:
    """
    Retrieve weather data from OpenWeather API for a given ZIP code.
    
    Args:
        zip_code: US ZIP code
        api_key: OpenWeather API key
        
    Returns:
        Dictionary with temperature and humidity, or None if error
    """
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "zip": zip_code,
        "appid": api_key,
        "units": "metric"  # Use Celsius for temperature
    }
    
    try:
        logger.info(f"Fetching weather data for ZIP code: {zip_code}")
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        
        logger.info(f"Received weather data - Temperature: {temperature}°F, Humidity: {humidity}%")
        return {
            "temperature": temperature,
            "humidity": humidity
        }
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching weather data: {e}")
        return None
    except KeyError as e:
        logger.error(f"Unexpected response format from OpenWeather API: {e}")
        return None


def submit_datadog_metrics(temperature: float, humidity: float, api_key: str, app_key: str):
    """
    Submit temperature and humidity as custom metrics to Datadog.
    
    Args:
        temperature: Temperature value in Fahrenheit
        humidity: Humidity percentage
        api_key: Datadog API key
        app_key: Datadog Application key
    """
    try:
        # Submit temperature metric
        api.Metric.send(
            metric='environment.temperature.outside',
            points=[(int(time.time()), temperature)],
            type='gauge'
        )
        logger.info(f"Submitted metric: environment.temperature.outside = {temperature}°F")
        
        # Submit humidity metric
        api.Metric.send(
            metric='environment.humidity.outside',
            points=[(int(time.time()), humidity)],
            type='gauge'
        )
        logger.info(f"Submitted metric: environment.humidity.outside = {humidity}%")
        
    except Exception as e:
        logger.error(f"Error submitting metrics to Datadog: {e}")


def main():
    """Main application loop."""
    global shutdown_flag
    
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Get environment variables
    openweather_api_key = os.getenv("OPENWEATHER_API_KEY")
    datadog_api_key = os.getenv("DATADOG_API_KEY")
    datadog_app_key = os.getenv("DATADOG_APP_KEY")
    zip_code = os.getenv("ZIP_CODE")
    
    # Validate required environment variables
    if not openweather_api_key:
        logger.error("OPENWEATHER_API_KEY environment variable is required")
        sys.exit(1)
    if not datadog_api_key:
        logger.error("DATADOG_API_KEY environment variable is required")
        sys.exit(1)
    if not datadog_app_key:
        logger.error("DATADOG_APP_KEY environment variable is required")
        sys.exit(1)
    if not zip_code:
        logger.error("ZIP_CODE environment variable is required")
        sys.exit(1)
    
    # Initialize Datadog
    options = {
        'api_key': datadog_api_key,
        'app_key': datadog_app_key
    }
    initialize(**options)
    logger.info("Datadog initialized successfully")
    
    logger.info("Starting weather monitoring service...")
    logger.info(f"Monitoring ZIP code: {zip_code}")
    logger.info("Press Ctrl+C to stop")
    
    # Main loop
    while not shutdown_flag:
        # Get weather data
        weather_data = get_weather_data(zip_code, openweather_api_key)
        
        if weather_data:
            # Submit metrics to Datadog
            submit_datadog_metrics(
                weather_data["temperature"],
                weather_data["humidity"],
                datadog_api_key,
                datadog_app_key
            )
        else:
            logger.warning("Skipping metric submission due to weather data fetch failure")
        
        # Wait 300 seconds before next iteration (unless shutdown requested)
        if not shutdown_flag:
            logger.info("Waiting 15 seconds until next check...")
            for _ in range(300):
                if shutdown_flag:
                    break
                time.sleep(1)
    
    logger.info("Weather monitoring service stopped")


if __name__ == "__main__":
    main()
