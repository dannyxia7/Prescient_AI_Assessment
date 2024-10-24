# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import requests
import time

# Define the API endpoint and parameters
api_key = "905bda20c026c0947a4e63bbb0db1135"  # Replace with your API key
city_name = "San Diego"  # Replace with the city you want to get weather for
base_url = "http://api.openweathermap.org/data/2.5/weather?"
max_requests_per_minute = 60  # Adjust based on your API plan (60 for free tier)

# Construct the final API URL
def get_weather_data(city, api_key):
    final_url = f"{base_url}q={city_name}&appid={api_key}&units=metric"

# Make the API request
    while True:
        response = requests.get(final_url)

    # Check for rate limit exceeded (HTTP 429)
        if response.status_code == 429:
            retry_after = int(
                response.headers.get('Retry-After', 60))  # default to 60 seconds if Retry-After is not provided
            print(f"Rate limit exceeded. Retrying after {retry_after} seconds.")
            time.sleep(retry_after)  # wait before retrying
        elif response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Error: {response.status_code}")
            return None

def make_requests_with_rate_limit(cities, api_key, max_requests_per_minute):
    interval = 60 / max_requests_per_minute  # Time interval between requests to avoid hitting the rate limit

    for city in cities:
        weather_data = get_weather_data(city, api_key)

        if weather_data:
            # Extract and print relevant data
            weather_description = weather_data['weather'][0]['description']
            temperature = weather_data['main']['temp']
            humidity = weather_data['main']['humidity']
            wind_speed = weather_data['wind']['speed']

            print(f"Weather in {city}:")
            print(f"Description: {weather_description}")
            print(f"Temperature: {temperature}°C")
            print(f"Humidity: {humidity}%")
            print(f"Wind Speed: {wind_speed} m/s")

        time.sleep(interval)  # Wait before making the next request

cities_to_check = ["San Diego", "Los Angeles", "New York"]  # Add more cities as needed
make_requests_with_rate_limit(cities_to_check, api_key, max_requests_per_minute)
