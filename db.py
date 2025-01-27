import requests


from pymongo import MongoClient

client = MongoClient("your_mongodb_connection_string")
db = client["your_database_name"]
collection = db["daily_overviews"]


def fetch_events():
    response = requests.get(f"https://raspberrypi.local:3002/events")
    if response.status_code == 200:
        return response.json()  # Assume your API returns a list of events
    else:
        return []
