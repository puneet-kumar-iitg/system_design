'''
Brute Force Cons :
    - notification params class is generic and hard coded which make it tight coupled.
    - NotificationStrategyFactory contains strategy dict which violet open/close principle.
    - No centralized retry mechanism implemented

Optimisation Approach :
    - Make retry a separate responsibility

    
'''
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable

@dataclass
class NotificationRequest(ABC):
    content : str

@dataclass
class EmailRequest(NotificationRequest):
    sender : str
    receiver : str
    subject : str | None

    def __str__(self):
        return f"reciever : {self.receiver}, subject : {self.subject} and content : {self.content}"

@dataclass
class SmsRequest(NotificationRequest):
    sender : str
    phone_number : str

    def __str__(self):
        return f"phone_number(reciever) : {self.phone_number} and content : {self.content}"

# @dataclass
# class PushRequest(NotificationRequest):
#     device_token: str
#     title: str

#     def __str__(self):
#         return f"device_token(reciever) : {self.device_token}, title : {self.title} and content : {self.content}"


class Notification(ABC):
    
    @abstractmethod
    def send(self, data: NotificationRequest):
        pass

class EmailNotification(Notification):

    def send(self, data : EmailRequest):
        if not isinstance(data, EmailRequest):
            raise ValueError(f"Email notification requires email request")
        print(f"Email Notification sent : {data}")

class SmsNotification(Notification):

    def send(self, data: SmsRequest):
        if not isinstance(data, SmsRequest):
            raise ValueError(f"Sms notification requires sms request")
        print(f"Sms Notification sent : {data}")


# class NotificationTemplate(ABC):
#     @abstractmethod
#     def render(self, data: dict):
#         pass

# class EmailNotificationTemplate(NotificationTemplate):

#     def render(self, data: dict):
#         return None

# class SmsNotificationTemplate(NotificationTemplate):

#     def render(self, data: dict):
#         return None
    

class RetryPolicy(ABC):

    @abstractmethod
    def execute(self, operation: Callable):
        pass
        
class SimpleRetryPolicy(RetryPolicy):

    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries

    def execute(self, operation):
        
        for attempt in range(self.max_retries + 1):
            try:
                return operation()
            except Exception:
                if attempt == self.max_retries:
                    raise ValueError(f"Operation failed after MAX_RETRIES : {attempt}")
                print(f"Retrying ... : attempt : {attempt}")


class NotificationChannelRegistry:

    def __init__(self):
        self._channel : dict[str, Notification] = {}

    def register(self, channel: str, notification : Notification):
        self._channel[channel] = notification

    def get(self, channel: str):
        notification_object = self._channel.get(channel)
        if not channel:
            raise ValueError(f"Unsupported Channel : {channel}")
        return notification_object
    
class NotificationService:

    def __init__(self, registry: NotificationChannelRegistry, retry_policy: RetryPolicy):
        self.registry = registry
        self.retry_policy = retry_policy

    def send(self, channel: str, request: NotificationRequest):
        notification = self.registry.get(channel)
        self.retry_policy.execute(
            lambda: notification.send(request)
        )



if __name__ == "__main__":
    registry = NotificationChannelRegistry()

    registry.register(
        "email",
        EmailNotification()
    )

    registry.register(
        "sms",
        SmsNotification()
    )

    retry_policy = SimpleRetryPolicy(max_retries=3)

    service = NotificationService(
        registry=registry,
        retry_policy=retry_policy
    )

    email_request = EmailRequest(sender="test@gmail.com", receiver="abc@gmail.com", subject="Email Notification", content="Hi there, How was your day?")

    service.send("email", email_request)