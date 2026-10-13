class Catalog:
    def __init__(self, products=()):
        self._products = list(products)

    def __len__(self):
        return len(self._products)

    def __iter__(self):
        return iter(self._products)

    def __getitem__(self, index):
        return self._products[index]

    def __contains__(self, flower):
        return flower in self._products

    def add(self, flower):
        if flower in self:
            raise ValueError('Товар с таким ID уже существует')
        self._products.append(flower)

    def sorted_by_price(self):
        return sorted(self._products)

    def find(self, identifier):
        for product in self._products:
            if product.id == int(identifier):
                return product
        raise ValueError('Товар не найден')
