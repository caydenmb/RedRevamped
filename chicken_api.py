import requests
import json
from datetime import datetime

api_key = "316a2f45bff17a887b8a37748e61ac06"
url_template = f"https://affiliates.chicken.gg/v1/referrals?key={api_key}&minTime={{min_time}}&maxTime={{max_time}}"
min_time = 1730419200000  # Fixed start time (October 31, 2024)
max_time = 1732867140000  # Fixed end time (November 28, 2024)
data_cache = {}

def log_message(level, message, data=None):
    """Logs messages with timestamps."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(json.dumps({"timestamp": timestamp, "level": level.upper(), "message": message, "data": data}))

def fetch_chicken_data():
    """Fetches data from Chicken.gg."""
    global data_cache
    try:
        url = url_template.format(min_time=min_time, max_time=max_time)
        response = requests.get(url)
        if response.status_code == 200:
            log_message("info", "Successfully fetched Chicken.gg data.")
            data_cache = response.json().get("referrals", [])
        else:
            log_message("error", f"Failed to fetch data. Status: {response.status_code}")
    except Exception as e:
        log_message("error", f"Exception: {e}")

def update_chicken_placeholders():
    """Processes and updates data for Chicken.gg."""
    global data_cache
    if isinstance(data_cache, list):
        sorted_data = sorted(data_cache, key=lambda x: x["wagerAmount"], reverse=True)
        data_cache = {
            f"top{i+1}": {
                "username": entry["displayName"],
                "wager": f"${entry['wagerAmount']:,.2f}"
            }
            for i, entry in enumerate(sorted_data[:11])
        }
        log_message("info", "Chicken.gg placeholders updated.")
