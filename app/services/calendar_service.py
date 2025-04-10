# import requests
# from pymongo import MongoClient
# from datetime import datetime, timedelta
# from config.env_config import MONGO_URI, EVENTS_API_URL

# client = MongoClient(MONGO_URI)
# db = client["test"]
# collection = db["calendar"]

# def findTodaysEvents():
#     today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
#     tomorrow = today + timedelta(days=1)

#     # Find entries with "start" field in the range of today
#     entries_today = collection.find({"start": {"$gte": today, "$lt": tomorrow}})

#     # Use count_documents to count the number of documents
#     if collection.count_documents({"start": {"$gte": today, "$lt": tomorrow}}) == 0:
#         # If no entries found, clear the collection
#         collection.delete_many({})
#         return fetch_and_store_events()
#     else:
#         return list(entries_today)

# def fetch_and_store_events():
#     response = requests.get(EVENTS_API_URL)
#     print('************')
#     print(response.json())
#     if response.status_code == 200:
#         if (response.json() == 'You have no events scheduled for today.'):
#             print("You have no events scheduled for today.")
#             return []
#         else:
#             events = response.json()
#             for event in events:
#                 collection.insert_one(event)
#             print("Events for today have been added to the database.")
#             return events
#     else:
#         print(f"Failed to fetch events. Status code: {response.status_code}")



# /services/calendar_service.py

from datetime import datetime

class CalendarService:
    def __init__(self):
        # Later you can initialize Google Calendar client here if you want
        pass

    def get_today_events(self):
        """Mocked for now: Return a list of today's events."""
        today = datetime.now().strftime("%A, %B %d")

        # Fake events
        events = [
            {
                "summary": "Morning Briefing",
                "start_time": "9:00 AM"
            },
            {
                "summary": "Workout Session",
                "start_time": "6:00 PM"
            }
        ]

        return events
