# -*- coding: utf-8 -*-
import requests
import datetime

# Your installation details
PANEL_COUNT = 12
PANEL_POWER_WP = 375
PANEL_AREA_M2 = 1.8  # m² per panel
PANEL_EFFICIENCY = 0.20  # 20%

TOTAL_AREA = PANEL_COUNT * PANEL_AREA_M2
EFFECTIVE_AREA = TOTAL_AREA * PANEL_EFFICIENCY

def fetch_solar_forecast(latitude, longitude):
    now = datetime.datetime.now(datetime.timezone.utc)
    start_date = now.strftime("%Y-%m-%d")
    end_date = (now + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitude}&longitude={longitude}&"
        f"hourly=shortwave_radiation&"
        f"start_date={start_date}&end_date={end_date}&timezone=auto"
    )

    try:
        response = requests.get(url)
        response.raise_for_status()
        solar_data = response.json()

        print(f"Solar Energy Forecast for Schweinfurt\n")
        hours = solar_data.get("hourly", {}).get("time", [])
        shortwave = solar_data.get("hourly", {}).get("shortwave_radiation", [])

        for time, sw in zip(hours, shortwave):
            estimated_power_watts = sw * EFFECTIVE_AREA  # W
            estimated_energy_kwh = estimated_power_watts / 1000  # kW

            readable_time = datetime.datetime.fromisoformat(time).strftime("%Y-%m-%d %H:%M")
            print(f"{readable_time} - Solar Production Estimate: {estimated_energy_kwh:.2f} kW")

    except requests.RequestException as e:
        print(f"Error fetching solar forecast: {e}")

def main():
    latitude = 50.0494   # Schweinfurt latitude
    longitude = 10.2218  # Schweinfurt longitude
    fetch_solar_forecast(latitude, longitude)

if __name__ == "__main__":
    main()
