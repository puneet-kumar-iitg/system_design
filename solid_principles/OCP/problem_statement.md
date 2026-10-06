Scenario: Payment Processing System

Initially, your application supports only:

Credit Card
UPI

class PaymentService:

    def process_payment(self, payment_type, amount):

        if payment_type == "CARD":
            print("Processing card payment")

        elif payment_type == "UPI":
            print("Processing UPI payment")


Later, business asks you to add:

PayPal
Net Banking
Wallet
Crypto

Every new payment method requires modifying this class.


Design it so that new payment methods can be added without changing PaymentService.