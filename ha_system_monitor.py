#!/usr/bin/env python3

import time
import socket
import json
import requests
import psutil
from datetime import datetime, timezone


# Load configuration

with open("config.json", "r") as file:
    CONFIG = json.load(file)

HA_URL = CONFIG["ha_url"]
HA_TOKEN = CONFIG["ha_token"]
DEVICE_NAME = CONFIG["name"]
ENTITY_PREFIX = CONFIG["entity_prefix"]
UPDATE_INTERVAL = CONFIG.get("update_interval", 60)
HOSTNAME = socket.gethostname()

HEADERS = {
    "Authorization": f"Bearer {HA_TOKEN}",
    "Content-Type": "application/json",
}

def send_sensor(entity_name, state, attributes=None):

    entity_id = f"sensor.{ENTITY_PREFIX}_{entity_name}"

    url = f"{HA_URL}/api/states/{entity_id}"

    payload = {
        "state": state,
        "attributes": {
            "friendly_name": f"{DEVICE_NAME} {entity_name.replace('_', ' ').title()}",
            "device_name": DEVICE_NAME,
            "host": HOSTNAME,
            **(attributes or {})
        }
    }

    try:
        response = requests.post(
            url,
            headers=HEADERS,
            json=payload,
            timeout=10
        )

        if response.status_code not in (200, 201):
            print(
                f"Failed updating {entity_id}: {response.status_code}"
            )

    except requests.exceptions.RequestException as error:
        print(
            f"Home Assistant connection error: {error}"
        )

def format_uptime(seconds):

    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60

    return f"{days}d {hours}h {minutes}m"

def collect_system_data():

    uptime_seconds = int(
        time.time() - psutil.boot_time()
    )

    return {

        "cpu": psutil.cpu_percent(interval=1),

        "memory": psutil.virtual_memory().percent,

        "disk": psutil.disk_usage("/").percent,

        "uptime_seconds": uptime_seconds,

        "uptime": format_uptime(uptime_seconds),

        "last_update": datetime.now(
            timezone.utc
        ).isoformat()

    }


def main():

    print(
        f"Starting Home Assistant monitor: {DEVICE_NAME}"
    )

    while True:

        data = collect_system_data()


        common = {
            "last_update": data["last_update"],
            "state_class": "measurement"
        }

        send_sensor(
            "cpu_usage",
            data["cpu"],
            {
                **common,
                "unit_of_measurement": "%"
            }
        )

        send_sensor(
            "memory_usage",
            data["memory"],
            {
                **common,
                "unit_of_measurement": "%"
            }
        )

        send_sensor(
            "disk_usage",
            data["disk"],
            {
                **common,
                "unit_of_measurement": "%"
            }
        )

        send_sensor(
            "uptime",
            data["uptime"],
            {
                "uptime_seconds": data["uptime_seconds"]
            }
        )

        print(
            f"{DEVICE_NAME}: "
            f"CPU {data['cpu']}% | "
            f"RAM {data['memory']}% | "
            f"Disk {data['disk']}%"
        )

        time.sleep(UPDATE_INTERVAL)

if __name__ == "__main__":
    main()
