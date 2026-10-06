Scenario: E-commerce Order Processing

You have an OrderService:

class OrderService:

    def create_order(self, data):
        pass

    def validate_order(self, data):
        pass

    def calculate_total(self, items):
        pass

    def save_order(self, order):
        pass

    def send_email(self, order):
        pass

    def generate_invoice(self, order):
        pass

    def update_inventory(self, order):
        pass

Refactor it using SRP.