# /services/failure_tracker_service.py

import datetime

class FailureTrackerService:
    def __init__(self):
        self.daily_failures = 0
        self.weekly_failures = {}
        self.current_week = datetime.date.today().isocalendar()[1]  # ISO week number

    def record_failure(self):
        """Called whenever a failure (disobedience, missed habits) happens."""
        today = datetime.date.today()

        # Update daily failures
        self.daily_failures += 1

        # Update weekly failures
        week = today.isocalendar()[1]
        if week != self.current_week:
            # New week started, reset
            self.current_week = week
            self.weekly_failures = {}
        
        if today not in self.weekly_failures:
            self.weekly_failures[today] = 0
        self.weekly_failures[today] += 1

    def reset_daily(self):
        """Called at end of day after evening ritual."""
        self.daily_failures = 0

    def get_daily_failures(self) -> int:
        return self.daily_failures

    def get_weekly_failures(self) -> int:
        return sum(self.weekly_failures.values())
