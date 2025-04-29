import argparse
import requests
import datetime
from geopy.geocoders import Nominatim

def resolve_location(location_name):
    geolocator = Nominatim(user_agent="solar-forecast-app")
    location = geolocator.geocode(location_name)
    if not location:
        raise ValueError(f"Location '{location_name}' could not be resolved.")
    return location.latitude, location.longitude

def fetch_solar_forecast(latitude, longitude, effective_area):
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

        hours = solar_data.get("hourly", {}).get("time", [])
        shortwave = solar_data.get("hourly", {}).get("shortwave_radiation", [])

        print("Time, Solar Production Estimate - kW")
        for time, sw in zip(hours, shortwave):
            estimated_power_watts = sw * effective_area  # W
            estimated_energy_kwh = estimated_power_watts / 1000  # kW

            readable_time = datetime.datetime.fromisoformat(time).strftime("%Y-%m-%d %H:%M")
            print(f"{readable_time},{estimated_energy_kwh:.2f}")

    except requests.RequestException as e:
        print(f"Error fetching solar forecast: {e}")

def main():
    parser = argparse.ArgumentParser(description="Estimate solar energy production.")
    parser.add_argument("location", nargs="?", help="City name or PLZ")
    parser.add_argument("panel_count", nargs="?", type=int, help="Number of solar panels")
    parser.add_argument("panel_power_wp", nargs="?", type=float, help="Panel power in Wp")
    parser.add_argument("panel_area_m2", nargs="?", type=float, help="Panel area in m²")
    parser.add_argument("panel_efficiency", nargs="?", type=float, help="Panel efficiency (e.g. 0.2 for 20%)")

    args = parser.parse_args()

    # Prompt if not passed
    location = args.location or input("Enter location (city or PLZ): ")
    panel_count = args.panel_count or int(input("Number of panels: "))
    panel_power_wp = args.panel_power_wp or float(input("Panel power (Wp): "))
    panel_area_m2 = args.panel_area_m2 or float(input("Panel area (m²): "))
    panel_efficiency = args.panel_efficiency or float(input("Panel efficiency (e.g. 0.2): "))

    total_area = panel_count * panel_area_m2
    effective_area = total_area * panel_efficiency

    lat, lon = resolve_location(location)
    fetch_solar_forecast(lat, lon, effective_area)

if __name__ == "__main__":
    main()
