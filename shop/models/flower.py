from functools import total_ordering


@total_ordering
class Flower:
    """Товар из каталога магазина."""

    def __init__(self, identifier, name, category, price, stock):
        self._id = int(identifier)
        self.name = name
        self.category = category
        self.price = price
        self.stock = stock

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError('Укажите название товара')
        self._name = value.strip()

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError('Укажите категорию')
        self._category = value.strip()

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if float(value) <= 0:
            raise ValueError('Цена должна быть больше нуля')
        self._price = float(value)

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, value):
        if int(value) < 0:
            raise ValueError('Остаток не может быть отрицательным')
        self._stock = int(value)

    def __eq__(self, other):
        if not isinstance(other, Flower):
            return NotImplemented
        return self.id == other.id

    def __lt__(self, other):
        if not isinstance(other, Flower):
            return NotImplemented
        return (self.price, self.name) < (other.price, other.name)

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return f'{self.name} — {self.price:.0f} ₽'

    def __repr__(self):
        return f'Flower({self.id}, {self.name!r}, {self.category!r}, {self.price}, {self.stock})'
