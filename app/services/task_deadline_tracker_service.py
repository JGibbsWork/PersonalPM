# /services/task_deadline_tracker_service.py

import datetime

class TaskDeadlineTrackerService:
    def __init__(self):
        # Track active tasks with their due times
        self.active_tasks = {}  # Format: {task_id: due_datetime}

    def register_task(self, task_id: str, hours_until_due: int = 24):
        """Register a new punishment task with a due date."""
        due_time = datetime.datetime.now() + datetime.timedelta(hours=hours_until_due)
        self.active_tasks[task_id] = due_time

    def complete_task(self, task_id: str):
        """Clear a task if user completed it."""
        if task_id in self.active_tasks:
            del self.active_tasks[task_id]

    def check_overdue_tasks(self, habitica_service) -> list:
        """Check which tasks are overdue and not completed."""
        overdue_task_ids = []

        for task_id, due_time in self.active_tasks.items():
            if datetime.datetime.now() > due_time:
                task = habitica_service.get_task_by_id(task_id)
                if task and not task.get('completed', False):
                    overdue_task_ids.append(task_id)

        return overdue_task_ids

    def purge_completed_tasks(self, habitica_service):
        """Clean up any tasks that were completed on time."""
        to_remove = []
        for task_id, due_time in self.active_tasks.items():
            task = habitica_service.get_task_by_id(task_id)
            if task and task.get('completed', False):
                to_remove.append(task_id)

        for task_id in to_remove:
            del self.active_tasks[task_id]
