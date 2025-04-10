# /services/escalation_manager_service.py

class EscalationManagerService:
    def __init__(self, punishment_generator_service, failure_tracker_service, penance_service):
        self.punishment_generator_service = punishment_generator_service
        self.failure_tracker_service = failure_tracker_service
        self.penance_service = penance_service

    def check_and_escalate(self, violation: str, preferences: list):
        """
        Check failure counts and penance completion. Escalate punishments appropriately.
        """
        daily_failures = self.failure_tracker_service.get_daily_failures()
        weekly_failures = self.failure_tracker_service.get_weekly_failures()

        # Check penance task status
        penance_failed = (
            self.penance_service.active_penance_task_id is not None and
            not self.penance_service.check_penance_completion()
        )

        severity = "light"

        if penance_failed:
            print("🚨 Penance task failed. Escalating punishment.")
            severity = "heavy"

        elif weekly_failures >= 5:
            print("🚨 5+ failures this week. Triggering FULL LOCKDOWN mode.")
            return "FULL_LOCKDOWN"

        elif weekly_failures >= 4:
            severity = "heavy"

        elif daily_failures >= 2:
            severity = "medium"

        else:
            severity = "light"

        # Generate new punishment
        punishment = self.punishment_generator_service.generate_punishment(
            violation=violation,
            severity=severity,
            preferences=preferences
        )

        return punishment
