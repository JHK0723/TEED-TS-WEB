import requests
from datetime import datetime, timedelta, timezone, time
import random

API_URL = "http://localhost:5000/log"  # Update this if your Flask app is running on a different port

def generate_random_logs(n=50):
    actions = ["entry", "exit"]
    today = datetime.now(timezone.utc).date()

    for _ in range(n):
        random_hour = random.randint(0, 23)
        random_minute = random.randint(0, 59)
        random_second = random.randint(0, 59)

        # Combine today's date with random time
        random_time = datetime.combine(today, time(random_hour, random_minute, random_second, tzinfo=timezone.utc))
        
        log = {
            "action": random.choice(actions),
            "timestamp": random_time.isoformat()
        }
        response = requests.post(API_URL, json=log)
        print(f"Sent log: {log}, Response: {response.status_code}, {response.text}")

if __name__ == "__main__":
    generate_random_logs(50)

