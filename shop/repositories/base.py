from abc import ABC, abstractmethod


class ShopRepository(ABC):
    @abstractmethod
    def load_products(self):
        pass

    @abstractmethod
    def save_product(self, flower):
        pass

    @abstractmethod
    def save_order(self, order):
        pass

    @abstractmethod
    def list_orders(self):
        pass
