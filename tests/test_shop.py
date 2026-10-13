import tempfile
import unittest
from datetime import datetime
from pathlib import Path

from shop.models.flower import Flower
from shop.models.order import Order, OrderItem
from shop.models.catalog import Catalog
from shop.repositories.base import ShopRepository
from shop.repositories.sqlite_repository import SQLiteShopRepository
from shop.services.session_service import SessionService
from shop.services.shop_service import ShopService


class ShopTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = SQLiteShopRepository(Path(self.tmp.name) / 'shop.db')
        self.service = ShopService(self.repo)

    def tearDown(self):
        self.tmp.cleanup()

    def test_catalog_has_twelve_products(self):
        self.assertEqual(len(self.service.catalog), 12)
        self.assertTrue(issubclass(SQLiteShopRepository, ShopRepository))

    def test_flower_comparison_and_properties(self):
        flowers = self.service.catalog.sorted_by_price()
        self.assertLessEqual(flowers[0].price, flowers[-1].price)
        with self.assertRaises(ValueError):
            flowers[0].price = -1
        with self.assertRaises(ValueError):
            flowers[0].stock = -1
        self.assertIn(flowers[0], self.service.catalog)

    def test_checkout_reduces_stock_and_persists_order(self):
        initial = self.service.catalog.find(1).stock
        self.service.add_to_basket(1, 2)
        self.assertEqual(len(self.service.basket), 1)
        number = self.service.checkout('Ирина')
        self.assertGreater(number, 0)
        self.assertEqual(SQLiteShopRepository(Path(self.tmp.name) / 'shop.db').load_products()[0].stock, initial - 2)
        self.assertEqual(self.repo.list_orders()[0][1], 'Ирина')

    def test_overstock_is_rejected(self):
        with self.assertRaises(ValueError):
            self.service.add_to_basket(1, 9999)

    def test_empty_basket_is_rejected(self):
        with self.assertRaises(ValueError):
            self.service.checkout('Покупатель')

    def test_stock_change_persists(self):
        self.service.change_stock(2, 24)
        self.assertEqual(self.repo.load_products()[1].stock, 24)

    def test_session_report_format(self):
        start = datetime(2026, 10, 13, 14, 15, 16)
        end = datetime(2026, 10, 13, 14, 20, 21)
        path = SessionService(Path(self.tmp.name), 'student', start).finish(end)
        report = path.read_text(encoding='utf-8')
        self.assertIn('login', report)
        self.assertIn('time_in', report)
        self.assertIn('time_out', report)
        self.assertIn('13.10.2026 14:15:16', report)
        self.assertIn('13.10.2026 14:20:21', report)


if __name__ == '__main__':
    unittest.main()
