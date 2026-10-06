from abc import ABC, abstractmethod

class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount):
        pass

class CardPaymentStrategy(PaymentStrategy):
    def pay(self, amount):
        print("Processing card payment")

class UpiPaymentStrategy(PaymentStrategy):
    def pay(self, amount):
        print("Processing UPI payment")

class PaymentService:
    def __init__(self, strategy: PaymentStrategy):
        self.strategy = strategy

    def process(self, amount):
        self.strategy.pay(amount)

if __name__ == "__main__":
    payment_service = PaymentService(CardPaymentStrategy())
    payment_service.process(100)

    payment_service = PaymentService(UpiPaymentStrategy())
    payment_service.process(100)
