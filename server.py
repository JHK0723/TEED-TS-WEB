from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv() 
client = MongoClient(os.environ.get("MONGODB_URI"))


app = Flask(__name__)

# MongoDB connection

client = MongoClient(os.environ.get("MONGODB_URI"))

db = client["teed_ts_db"]
collection = db["entry_exit_logs"]

@app.route("/")
def home():
    logs = collection.find().sort("timestamp", -1)
    total_entries = collection.count_documents({"action": "entry"})
    total_exits = collection.count_documents({"action": "exit"})
    current_inside = total_entries - total_exits
    return render_template("index.html", logs=logs, total_entries=total_entries, total_exits=total_exits, current_inside=current_inside)

from datetime import datetime

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

from datetime import datetime
from collections import Counter
from flask import jsonify


if __name__ == "__main__":
    app.run(debug=True)

