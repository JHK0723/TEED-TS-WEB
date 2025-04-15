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

@app.route("/log/entry", methods=["POST"])
def log_entry():
    

    log = {
        "action": "entry",
        "timestamp": datetime.now().isoformat()
    }
    collection.insert_one(log)
    socketio.emit('update_data', {"message": "New entry logged"})

@app.route("/log/exit", methods=["POST"])
def log_exit():
    log = {
        "action": "exit",
        "timestamp": datetime.now().isoformat()
    }
    collection.insert_one(log)
    socketio.emit('update_data', {"message": "New exit logged"})


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
        "$addFields": {
            "timestamp": {
                "$cond": [
                    { "$not": [{ "$eq": [{ "$type": "$timestamp" }, "date"] }] },
                    { "$toDate": "$timestamp" },
                    "$timestamp"
                ]
            }
        }
    },
    {
        "$group": {
            "_id": {
                "year": { "$year": "$timestamp" },
                "month": { "$month": "$timestamp" },
                "day": { "$dayOfMonth": "$timestamp" },
                "hour": { "$hour": "$timestamp" },
                "minute": {
                    "$subtract": [
                        { "$minute": "$timestamp" },
                        { "$mod": [{ "$minute": "$timestamp" }, 5] }
                    ]
                },
                "action": "$action"
            },
            "count": { "$sum": 1 }
        }
    },
    {
        "$sort": {
            "_id.year": 1,
            "_id.month": 1,
            "_id.day": 1,
            "_id.hour": 1,
            "_id.minute": 1
        }
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


if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)  # Accessible from all network interfaces
