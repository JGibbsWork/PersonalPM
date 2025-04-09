import json
import os
import datetime

HABITS_FILE = "data/habits.json"

def load_habits():
    if not os.path.exists(HABITS_FILE):
        return {"habits": []}
    with open(HABITS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_habits(habits_data):
    with open(HABITS_FILE, "w", encoding="utf-8") as f:
        json.dump(habits_data, f, indent=2)

def ask_about_habits(habits_data):
    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%A")
    updates = []

    print(f"\n🔍 Checking habits for YESTERDAY ({yesterday}):\n")

    for habit in habits_data["habits"]:
        if yesterday in habit["target_days"]:
            while True:
                answer = input(f"Did you complete the habit '{habit['name']}' yesterday? (yes/no): ").strip().lower()
                if answer in ["yes", "no"]:
                    break
                print("Invalid input. Please answer 'yes' or 'no'.")
            
            if answer == "yes":
                habit["success_count"] += 1
                habit["last_status"] = "success"
            else:
                habit["failure_count"] += 1
                habit["last_status"] = "failure"
            habit["last_checked"] = str(datetime.datetime.now().date())
            updates.append((habit["name"], habit["last_status"]))
        else:
            print(f"(Skipping '{habit['name']}' — not tracked on {yesterday})")

    return habits_data, updates

def generate_habit_summary(habits_data):
    summary = "Habit Compliance Summary:\n"
    for habit in habits_data["habits"]:
        if habit["last_status"]:
            summary += f"- {habit['name']}: {habit['last_status'].capitalize()} ({habit['success_count']} successes, {habit['failure_count']} failures)\n"
    return summary
