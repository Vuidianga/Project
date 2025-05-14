from datetime import datetime, timedelta, time

# Tariffs in ?/kWh
LOW_TARIFF = 0.0431
STANDARD_TARIFF = 0.1077
HIGH_TARIFF = 0.1435

# Define tariff time windows
LOW_HOURS = [(time(0, 0), time(3, 0))]
HIGH_HOURS = [(time(11, 30), time(12, 30)), (time(17, 0), time(18, 0))]

# Timezone offset (you can automate this if needed)
TIMEZONE = "+02:00"  # Change if DST shifts or for other German zones

# Match-case style (Python 3.10+)
def get_tariff(t: time) -> float:
    match t:
        case _ if time(11, 30) <= t < time(12, 30):
            return HIGH_TARIFF
        case _ if time(17, 0) <= t < time(18, 0):
            return HIGH_TARIFF
        case _ if time(0, 0) <= t < time(3, 0):
            return LOW_TARIFF
        case _:
            return STANDARD_TARIFF

# Align current time to the next 15-minute mark
now = datetime.now().replace(second=0, microsecond=0)
minute = now.minute
remainder = (60 - minute % 60) % 60
start_time = now + timedelta(minutes=remainder)

# Generate 96 intervals (15 min for 24h)
print('Date,Time,Timezone,Grid_prices[EUR/kWh]')
for i in range(60):
    timestamp = start_time + timedelta(minutes=60 * i)
    date_str = timestamp.strftime('%Y-%m-%d')
    time_str = timestamp.strftime('%H:%M')
    price = get_tariff(timestamp.time())
    print(f"{date_str},{time_str},{TIMEZONE},{price}")
