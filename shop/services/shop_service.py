from shop.models.catalog import Catalog
from shop.models.order import Order, OrderItem


class ShopService:
    def __init__(self, repository):
        self.repository = repository
        self.catalog = Catalog(repository.load_products())
        self._basket = []

    @property
    def basket(self):
        return tuple(self._basket)

    @property
    def basket_total(self):
        return sum(item.amount for item in self._basket)

    def filtered_products(self, term='', category='Все', sort=False):
        products = list(self.catalog.sorted_by_price() if sort else self.catalog)
        return [flower for flower in products
                if term.lower() in flower.name.lower()
                and (category == 'Все' or flower.category == category)]

    def add_to_basket(self, product_id, quantity):
        flower = self.catalog.find(product_id)
        quantity = int(quantity)
        if quantity < 1:
            raise ValueError('Укажите количество')
        existing = next((item for item in self._basket if item.flower == flower), None)
        previous = existing.quantity if existing else 0
        if previous + quantity > flower.stock:
            raise ValueError('На складе недостаточно цветов')
        if existing:
            existing.quantity += quantity
        else:
            self._basket.append(OrderItem(flower, quantity))

    def remove_from_basket(self, product_id):
        self._basket = [item for item in self._basket if item.flower.id != int(product_id)]

    def checkout(self, customer):
        order = Order(customer, self._basket)
        number = self.repository.save_order(order)
        for item in order:
            item.flower.stock -= item.quantity
        self._basket.clear()
        return number

    def change_stock(self, product_id, stock):
        product = self.catalog.find(product_id)
        product.stock = stock
        self.repository.save_product(product)
