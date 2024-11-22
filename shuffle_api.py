import requests
import json
from datetime import datetime

api_key = "f45f746d-b021-494d-b9b6-b47628ee5cc9"
url_template = f"https://affiliate.shuffle.com/stats/{api_key}?startTime={{start_time}}&endTime={{end_time}}"
start_time = 1728881970  # Fixed epoch time (October 13, 2024)
data_cache = {}

def log_message(level, message, data=None):
    """Logs messages with timestamps."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(json.dumps({"timestamp": timestamp, "level": level.upper(), "message": message, "data": data}))

def fetch_shuffle_data():
    """Fetches data from Shuffle.com."""
    global data_cache
    try:
        end_time = int(datetime.now().timestamp() - 10)  # Current time - 10 seconds
        url = url_template.format(start_time=start_time, end_time=end_time)
        response = requests.get(url)
        if response.status_code == 200:
            log_message("info", "Successfully fetched Shuffle.com data.")
            data_cache = response.json()
        else:
            log_message("error", f"Failed to fetch data. Status: {response.status_code}")
    except Exception as e:
        log_message("error", f"Exception: {e}")

def update_shuffle_placeholders():
    """Processes and updates data for Shuffle.com."""
    global data_cache
    if isinstance(data_cache, list):
        sorted_data = sorted(data_cache, key=lambda x: x["wagerAmount"], reverse=True)
        data_cache = {
            f"top{i+1}": {
                "username": entry["username"],
                "wager": f"${entry['wagerAmount']:,.2f}"
            }
            for i, entry in enumerate(sorted_data[:11])
        }
        log_message("info", "Shuffle.com placeholders updated.")
