import requests
import datetime

def fetch_weather(latitude, longitude):
    now = datetime.datetime.now(datetime.timezone.utc)
    start_date = now.strftime("%Y-%m-%d")
    end_date = (now + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitude}&longitude={longitude}&"
        f"hourly=temperature_2m,weathercode&"
        f"start_date={start_date}&end_date={end_date}&timezone=auto"
    )

    try:
        response = requests.get(url)
        response.raise_for_status()
        weather_data = response.json()

        timezone = "+02:00"
        hours = weather_data.get("hourly", {}).get("time", [])
        temperatures = weather_data.get("hourly", {}).get("temperature_2m", [])
        weather_codes = weather_data.get("hourly", {}).get("weathercode", [])
<<<<<<< HEAD
<<<<<<< HEAD
        print("Time,Temperature (degree C) ,Weather condition")
=======
        print("Date,Time,Timezone,Temperature (degree C) ,Weather condition")
>>>>>>> 1a7402d1e953f386110a1fb376e3dcad00e997cc
=======
        print("Date,Time,Timezone,Temperature (degree C) ,Weather condition")
>>>>>>> 1a7402d1e953f386110a1fb376e3dcad00e997cc

        for time, temp, code in zip(hours, temperatures, weather_codes):
            readable_time = datetime.datetime.fromisoformat(time).strftime("%Y-%m-%d %H:%M")
            condition = weather_code_to_description(code)
            print(f"{readable_time[:10]},{readable_time[11:]},{timezone},{temp},{condition}")
=======
            print(f"{readable_time[:10]},{readable_time[11:]},{timezone},{temp},{condition}")
>>>>>>> 1a7402d1e953f386110a1fb376e3dcad00e997cc

    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")

def weather_code_to_description(code):
    """Translate Open-Meteo weather codes to human readable descriptions"""
    mapping = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snow fall",
        73: "Moderate snow fall",
        75: "Heavy snow fall",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail"
    }
    return mapping.get(code, "Unknown")

def main():
    latitude = 50.0494   # Schweinfurt latitude
    longitude = 10.2218  # Schweinfurt longitude
    fetch_weather(latitude, longitude)

if __name__ == "__main__":
    main()
