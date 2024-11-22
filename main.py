import os
import json
import threading
from flask import Flask, render_template, jsonify, request, abort, redirect, url_for
from shuffle_api import fetch_shuffle_data, update_shuffle_placeholders
from chicken_api import fetch_chicken_data, update_chicken_placeholders
from datetime import datetime

app = Flask(__name__, static_folder="static", template_folder=".")

# Admin-controlled toggles for enabling/disabling races
enabled_races = {"shuffle": True, "chicken": True}

# Securely Obfuscated Admin IP
OBFUSCATED_IP = "".join([chr(ord(c) + 2) for c in "69.162.253.60"])

# Logging Function
LOG_FILE = "logs/app.log"
os.makedirs("logs", exist_ok=True)

def log_message(level, message, data=None):
    """Logs messages in JSON format."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = {"timestamp": timestamp, "level": level.upper(), "message": message, "data": data}
    print(f"{level.upper()}: {message}")
    with open(LOG_FILE, "a") as log_file:
        log_file.write(json.dumps(log_entry) + "\n")

# Update Data Cache Every 90 Seconds
def update_data():
    """Fetches and processes data for Shuffle.com and Chicken.gg."""
    if enabled_races["shuffle"]:
        fetch_shuffle_data()
        update_shuffle_placeholders()
    if enabled_races["chicken"]:
        fetch_chicken_data()
        update_chicken_placeholders()
    log_message("info", "Data updated successfully.")

def schedule_updates():
    """Schedules updates every 90 seconds."""
    threading.Timer(90, schedule_updates).start()
    update_data()

# Routes
@app.route("/")
def index():
    """Redirects to Shuffle.com page if enabled, otherwise Chicken.gg."""
    if enabled_races["shuffle"]:
        return redirect(url_for("shuffle_page"))
    elif enabled_races["chicken"]:
        return redirect(url_for("chicken_page"))
    else:
        return render_template("404.html"), 404

@app.route("/shuffle")
def shuffle_page():
    """Renders Shuffle.com leaderboard page."""
    if not enabled_races["shuffle"]:
        abort(403)
    return render_template("shuffle.html")

@app.route("/chicken")
def chicken_page():
    """Renders Chicken.gg leaderboard page."""
    if not enabled_races["chicken"]:
        abort(403)
    return render_template("chicken.html")

@app.route("/toggle/<race>", methods=["POST"])
def toggle_race(race):
    """Toggles visibility of a race page for admins."""
    client_ip = request.remote_addr
    allowed_ip = "".join([chr(ord(c) - 2) for c in OBFUSCATED_IP])
    if client_ip != allowed_ip:
        log_message("warning", "Unauthorized toggle attempt", {"client_ip": client_ip})
        abort(403)
    if race in enabled_races:
        enabled_races[race] = not enabled_races[race]
        status = "enabled" if enabled_races[race] else "disabled"
        log_message("info", f"Toggled {race.capitalize()} Race", {"status": status})
        return jsonify({race: enabled_races[race]})
    abort(404)

@app.errorhandler(404)
def page_not_found(e):
    """Handles 404 errors."""
    log_message("warning", "404 Error - Page not found")
    return render_template("404.html"), 404

if __name__ == "__main__":
    schedule_updates()
    app.run(host="0.0.0.0", port=8080)
