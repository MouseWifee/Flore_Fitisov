from datetime import datetime


class OrderItem:
    def __init__(self, flower, quantity):
        self.flower = flower
        self.quantity = quantity

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        if int(value) <= 0:
            raise ValueError('Количество должно быть положительным')
        self._quantity = int(value)

    @property
    def amount(self):
        return round(self.flower.price * self.quantity, 2)


class Order:
    def __init__(self, customer, items, created_at=None):
        if not customer.strip():
            raise ValueError('Укажите имя покупателя')
        if not items:
            raise ValueError('Корзина пуста')
        self.customer = customer.strip()
        self.items = tuple(items)
        self.created_at = created_at or datetime.now()

    @property
    def total(self):
        return round(sum(item.amount for item in self.items), 2)

    def __len__(self):
        return sum(item.quantity for item in self.items)

    def __iter__(self):
        return iter(self.items)

    def __contains__(self, flower):
        return any(item.flower == flower for item in self.items)
