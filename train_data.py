import requests
from datetime import datetime, timedelta, timezone
import random

API_URL = "http://localhost:5000/log"  # Update this if your Flask app is running on a different port

def generate_random_logs(n=50):
    actions = ["entry", "exit"]
    now = datetime.now(timezone.utc)  # Use timezone-aware datetime
    
    for _ in range(n):
        random_time = now - timedelta(days=random.randint(0, 5), hours=random.randint(0, 23), minutes=random.randint(0, 59))
        log = {
            "action": random.choice(actions),
            "timestamp": random_time.isoformat()
        }
        response = requests.post(API_URL, json=log)
        print(f"Sent log: {log}, Response: {response.status_code}, {response.text}")

if __name__ == "__main__":
    generate_random_logs(50)
