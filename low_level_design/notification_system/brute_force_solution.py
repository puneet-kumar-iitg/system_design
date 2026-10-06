'''
brute force Approach :
    Cons :
        - notification params class is generic and hard coded which make it tight coupled.
        - NotificationStrategyFactory contains strategy dict which violet open/close principle.
        - No centralized retry mechanism implemented
'''

from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class NotificationParams:
    sender : str
    receiver : str
    subject : str | None
    content : str

    def __str__(self):
        return f"reciever : {self.receiver}, subject : {self.subject} and content : {self.content}"


class Notification(ABC):
    
    @abstractmethod
    def send(self, data: NotificationParams):
        pass

class EmailNotification(Notification):

    def send(self, data : NotificationParams):
        print(f"Email Notification sent : {data}")

class SmsNotification(Notification):

    def send(self, data: NotificationParams):
        print(f"Sms Notification sent : {data}")


class NotificationStrategyFactory:

    STRATEGIES = {
        "email": EmailNotification,
        "sms": SmsNotification
    }

    def __init__(self, channel: str):
        self.channel = channel

    def get_strategy(self):
        strategy = self.STRATEGIES.get(self.channel)
        if not strategy:
            raise ValueError(f"Unsupported notification channel : {self.channel}")
        return strategy()


if __name__ == "__main__":
    channel = "email"
    channel_object = NotificationStrategyFactory(channel).get_strategy()
    print(type(channel_object))
    np =  NotificationParams(sender="test@gmail.com", receiver="abc@gmail.com", subject="Email Notification", content="Hi there, How was your day?")
    channel_object.send(np)


    

    

    
        



