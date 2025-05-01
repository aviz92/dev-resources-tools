# dependency_injection.py

# 📌 Principle:
# Dependency Injection is a design pattern where a class receives its dependencies from an external source rather than creating them internally.
# This promotes loose coupling and makes the code more flexible and testable.

import logging
from abc import ABC


class NotificationService(ABC):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def send_message(self, recipient: str, message: str):
        self.logger.info(f"[EmailService] Sending email to {recipient}: {message}")


class EmailService(NotificationService):
    def send_message(self, recipient: str, message: str):
        self.logger.info(f"[EmailService] Sending email to {recipient}: {message}")


class SMSService(NotificationService):
    def send_message(self, recipient: str, message: str):
        self.logger.info(f"[SMSService] Sending SMS to {recipient}: {message}")


class UserNotifier:
    def __init__(self, notification_service):  # Dependency injected via constructor
        self.notification_service = notification_service

    def notify_user(self, recipient: str, message: str):
        self.notification_service.send_message(recipient, message)


def main():
    # You can easily swap dependencies
    email_service = EmailService()
    notifier = UserNotifier(notification_service=email_service)  # Injecting EmailService
    notifier.notify_user("user@example.com", "Welcome to the platform!")

    print("\nSwitching to SMS service:\n")
    sms_service = SMSService()
    notifier = UserNotifier(notification_service=sms_service)  # Injecting SMSService
    notifier.notify_user("123-456-7890", "Welcome to the platform via SMS!")


if __name__ == "__main__":
    main()
