import requests
from datetime import datetime, timedelta

def fetch_coordinates(city_name):
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1"
    response = requests.get(geo_url)
    
    if response.status_code == 200:
        geo_data = response.json()
        if geo_data.get('results'):
            lat = geo_data['results'][0]['latitude']
            lon = geo_data['results'][0]['longitude']
            return lat, lon
        else:
            print("City not found.")
            return None, None
    else:
        print("Error fetching coordinates.")
        return None, None

def fetch_weather(lat, lon):
    now = datetime.utcnow()
    tomorrow = now + timedelta(hours=24)
    
    start = now.strftime('%Y-%m-%dT%H:00')
    end = tomorrow.strftime('%Y-%m-%dT%H:00')
    
    weather_url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&hourly=temperature_2m"
        f"&start={start}&end={end}"
        f"&timezone=auto"
    )
    
    response = requests.get(weather_url)
    
    if response.status_code == 200:
        weather_data = response.json()
        hours = weather_data.get('hourly', {}).get('time', [])
        temperatures = weather_data.get('hourly', {}).get('temperature_2m', [])
        
        if hours and temperatures:
            for time, temp in zip(hours, temperatures):
                print(f"{time} → {temp}°C")
        else:
            print("No weather data available.")
    else:
        print("Error fetching weather.")

def main():
    city = input("Enter your city name: ")
    lat, lon = fetch_coordinates(city)
    
    if lat is not None and lon is not None:
        print(f"Coordinates for {city}: {lat}, {lon}")
        print("Fetching 24-hour weather forecast...\n")
        fetch_weather(lat, lon)

if __name__ == "__main__":
    main()
