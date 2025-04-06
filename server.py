import eventlet
eventlet.monkey_patch()  # Must be first for compatibility with PyMongo and Flask-SocketIO

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from pymongo import MongoClient
import datetime as dt
from datetime import datetime
import os
from dotenv import load_dotenv
from pathlib import Path
import threading
# import serial  # Uncomment when using actual hardware
# import re
# import requests
# import time

# Load environment variables
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# MongoDB connection
client = MongoClient(os.environ.get("MONGODB_URI"))
db = client["teed_ts_db"]
collection = db["entry_exit_logs"]

# Initialize Flask app and SocketIO
app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet')  # async_mode is required for real-time updates

@app.route("/")
def home():
    logs = collection.find().sort("timestamp", -1)
    total_entries = collection.count_documents({"action": "entry"})
    total_exits = collection.count_documents({"action": "exit"})
    current_inside = total_entries - total_exits
    return render_template("index.html", logs=logs, total_entries=total_entries, total_exits=total_exits, current_inside=current_inside)

@app.route("/log", methods=["POST"])
def log_entry_exit():
    data = request.json
    if "action" not in data or data["action"] not in ["entry", "exit"]:
        return jsonify({"error": "Invalid action"}), 400

    try:
        timestamp = datetime.fromisoformat(data["timestamp"])  # Parse ISO timestamp
    except (KeyError, ValueError):
        return jsonify({"error": "Invalid or missing timestamp"}), 400

    log = {
        "action": data["action"],
        "timestamp": timestamp
    }
    collection.insert_one(log)

    # Emit update to all connected clients
    socketio.emit('update_data', {"message": "New log entry added"})
    print("📡 update_data emitted to clients")

    return jsonify({"message": "Logged successfully"}), 201

@app.route("/logs", methods=["GET"])
def get_logs():
    logs = list(collection.find({}, {"_id": 0}).sort("timestamp", -1))
    return jsonify(logs)

@app.route("/analytics", methods=["GET"])
def analytics():
    total_entries = collection.count_documents({"action": "entry"})
    total_exits = collection.count_documents({"action": "exit"})
    current_inside = total_entries - total_exits
    return jsonify({
        "total_entries": total_entries,
        "total_exits": total_exits,
        "current_inside": current_inside
    })

@app.route("/analytics/interval", methods=["GET"])
def interval_analytics():
    try:
        pipeline = [
            {
                "$group": {
                    "_id": {
                        "year": {"$year": "$timestamp"},
                        "month": {"$month": "$timestamp"},
                        "day": {"$dayOfMonth": "$timestamp"},
                        "hour": {"$hour": "$timestamp"},
                        "minute": {"$subtract": [
                            {"$minute": "$timestamp"},
                            {"$mod": [{"$minute": "$timestamp"}, 5]}
                        ]},
                        "action": "$action"
                    },
                    "count": {"$sum": 1}
                }
            },
            {
                "$sort": {"_id.year": 1, "_id.month": 1, "_id.day": 1, "_id.hour": 1, "_id.minute": 1}
            }
        ]
        results = collection.aggregate(pipeline)

        data = {}
        for entry in results:
            time_key = f"{entry['_id']['year']}-{entry['_id']['month']:02d}-{entry['_id']['day']:02d} {entry['_id']['hour']:02d}:{entry['_id']['minute']:02d}"
            action_type = entry["_id"]["action"]
            if time_key not in data:
                data[time_key] = {"entry": 0, "exit": 0}
            data[time_key][action_type] = entry["count"]

        return jsonify(data)

    except Exception as e:
        print("Error in /analytics/interval:", e)
        return jsonify({"error": str(e)}), 500

# ----------------- OPTIONAL HARDWARE INTEGRATION (SERIAL LISTENER) -----------------
# Uncomment below to use real-time logs from Arduino via serial

# def serial_listener():
#     ser = serial.Serial('COM5', 115200)  # Update port as needed
#     pattern = re.compile(r"(Entry|Exit) detected at.*?(\d+) hr : (\d+) min : (\d+) sec")
#     while True:
#         if ser.in_waiting > 0:
#             line = ser.readline().decode('utf-8', errors='ignore').strip()
#             match = pattern.search(line)
#             if match:
#                 action = 'entry' if match.group(1) == 'Entry' else 'exit'
#                 now = datetime.now().replace(
#                     hour=int(match.group(2)),
#                     minute=int(match.group(3)),
#                     second=int(match.group(4)),
#                     microsecond=0
#                 )
#                 log = {"action": action, "timestamp": now.isoformat()}
#                 try:
#                     requests.post("http://localhost:5000/log", json=log)
#                     print(f"Sent via serial: {log}")
#                 except Exception as e:
#                     print(f"Failed to send log: {e}")
#         time.sleep(1)

# ------------------------------------------------------------------------------------

if __name__ == "__main__":
    # Enable this when testing with hardware
    # threading.Thread(target=serial_listener, daemon=True).start()
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)  # Accessible from all network interfaces
