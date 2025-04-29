#!/usr/bin/env python3

import time
import os
import sys

BATTERY_FILE = r"C:\Users\asantee\.node-red\projects\Project\battery_file"

def save_battery_state(level, status):
    with open(BATTERY_FILE, "w") as f:
        f.write(f"{level},{status}")

def load_battery_state():
    if not os.path.exists(BATTERY_FILE):
        return 100.0, "idle"  # default battery level
    with open(BATTERY_FILE, "r") as f:
        content = f.read().strip()
        level_str, status = content.split(",")
        return float(level_str), status

def charging(battery_level, switch, charging_power, battery_capacity):
    is_charging = False
    while battery_level < 100 and switch:
        battery_level += (charging_power / battery_capacity) * 100 / 3600
        if battery_level > 100:
            battery_level = 100
        print(f"Battery level is now {battery_level:.2f}%")
        is_charging = True
        save_battery_state(battery_level, "charging")
        time.sleep(0.1)
    return battery_level, is_charging

def discharging(battery_level, switch, discharging_power, battery_capacity):
    is_discharging = False
    while battery_level > 0 and switch:
        battery_level -= (discharging_power / battery_capacity) * 100 / 3600
        if battery_level < 0:
            battery_level = 0
        print(f"Battery level is now {battery_level:.2f}%")
        is_discharging = True
        save_battery_state(battery_level, "discharging")
        time.sleep(0.1)
    return battery_level, is_discharging

def battery_status():
    level, status = load_battery_state()
    print(f"Battery level is now {level:.2f}%")
    print(f"Status: {status.capitalize()}")


def battery(_command, _status):
    level, previous_status = load_battery_state()
    charging_, discharging_ = False, False
    _is_charging = False
    _is_discharging = False

    if _status == "charging":
        _is_charging = True
    elif _status == "discharging":
        _is_discharging = True

    if _command == 1 and not _is_charging:
        level, charging_ = charging(level, True, 1000, 7000)
    elif _command == 2 and not _is_discharging:
        level, discharging_ = discharging(level, True, 1000, 7000)
    elif _command == 3:
        battery_status()


    new_status = "charging" if charging_ else "discharging" if discharging_ else "idle"
    save_battery_state(level, new_status)

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in ['1', '2', '3']:
        print("Usage: ./battery [1=Charge | 2=Discharge | 3=Status]")
        sys.exit(1)
    _, status = load_battery_state()
    command = int(sys.argv[1])
    battery(command, status)
