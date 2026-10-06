
class OrderValidator:
    def validate(self, data):
        pass

class PricingService:
    def calculate_total(self, items):
        pass

class OrderRepository:
    def save(self, order):
        pass

class NotificationService:
    def send_email(self, order):
        pass

class InvoiceService:
    def generate_invoice(self, order):
        pass

class InventoryService:
    def update(self, order):
        pass

class OrderService:
    def __init__(self, validator: OrderValidator, pricing_service: PricingService, repository: OrderRepository, notification_service: NotificationService, invoice_service: InvoiceService, inventory_service: InventoryService):
        self.validator = validator
        self.pricing_service = pricing_service
        self.repository = repository
        self.notification_service = notification_service
        self.invoice_service = invoice_service
        self.inventory_service = inventory_service

    def create(self, data):
        self.validator.validate(data)
        total = self.pricing_service.calculate_total(data['items'])

        order = {"data": data, "total": total}

        self.repository.save(order)
        self.notification_service.send_email(order)
        self.invoice_service.generate_invoice(order)
        self.inventory_service.update(order)
        return order


if __name__ == "__main__":
    validator = OrderValidator()
    pricing_service = PricingService()
    repository = OrderRepository()
    notification_service = NotificationService()
    invoice_service = InvoiceService()
    inventory_service = InventoryService()
    order_service = OrderService(validator, pricing_service, repository, notification_service, invoice_service, inventory_service)
    order = order_service.create({"items": [{"name": "Product 1", "price": 100}, {"name": "Product 2", "price": 200}]})
    print("Order created: ", order)