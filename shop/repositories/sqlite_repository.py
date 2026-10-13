import sqlite3
from pathlib import Path

from shop.models.flower import Flower
from shop.repositories.base import ShopRepository


START_PRODUCTS = (
    ('Пионовидные розы', 'Букеты', 3900, 12),
    ('Нежная гортензия', 'Букеты', 2850, 9),
    ('Белые тюльпаны', 'Цветы', 190, 95),
    ('Розовые пионы', 'Цветы', 450, 46),
    ('Роза Эквадор', 'Цветы', 320, 120),
    ('Эустома', 'Цветы', 260, 75),
    ('Ромашковое поле', 'Букеты', 2400, 15),
    ('Солнечный день', 'Букеты', 3100, 11),
    ('Лавандовый сад', 'Букеты', 3500, 8),
    ('Хризантема', 'Цветы', 240, 80),
    ('Альстромерия', 'Цветы', 210, 62),
    ('Нежный рассвет', 'Букеты', 4300, 7),
)


class SQLiteShopRepository(ShopRepository):
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connection(self):
        connection = sqlite3.connect(self.path)
        connection.execute('PRAGMA foreign_keys = ON')
        return connection

    def _initialize(self):
        with self._connection() as connection:
            connection.execute('CREATE TABLE IF NOT EXISTS products ('
                               'id INTEGER PRIMARY KEY, name TEXT NOT NULL, '
                               'category TEXT NOT NULL, price REAL NOT NULL, stock INTEGER NOT NULL)')
            connection.execute('CREATE TABLE IF NOT EXISTS orders ('
                               'id INTEGER PRIMARY KEY AUTOINCREMENT, customer TEXT NOT NULL, '
                               'created_at TEXT NOT NULL, total REAL NOT NULL)')
            connection.execute('CREATE TABLE IF NOT EXISTS order_items ('
                               'id INTEGER PRIMARY KEY AUTOINCREMENT, order_id INTEGER NOT NULL, '
                               'product_id INTEGER NOT NULL, product_name TEXT NOT NULL, '
                               'quantity INTEGER NOT NULL, unit_price REAL NOT NULL, '
                               'FOREIGN KEY(order_id) REFERENCES orders(id))')
            count = connection.execute('SELECT COUNT(*) FROM products').fetchone()[0]
            if count == 0:
                connection.executemany('INSERT INTO products(name, category, price, stock) VALUES(?,?,?,?)', START_PRODUCTS)

    def load_products(self):
        with self._connection() as connection:
            rows = connection.execute('SELECT id, name, category, price, stock FROM products ORDER BY id').fetchall()
        return [Flower(*row) for row in rows]

    def save_product(self, flower):
        with self._connection() as connection:
            connection.execute('UPDATE products SET name=?, category=?, price=?, stock=? WHERE id=?',
                               (flower.name, flower.category, flower.price, flower.stock, flower.id))

    def save_order(self, order):
        with self._connection() as connection:
            for item in order:
                current = connection.execute('SELECT stock FROM products WHERE id=?', (item.flower.id,)).fetchone()
                if current is None or current[0] < item.quantity:
                    raise ValueError(f'Недостаточно товара: {item.flower.name}')
            cursor = connection.execute('INSERT INTO orders(customer, created_at, total) VALUES (?,?,?)',
                                        (order.customer, order.created_at.strftime('%d.%m.%Y %H:%M:%S'), order.total))
            order_id = cursor.lastrowid
            for item in order:
                connection.execute('INSERT INTO order_items(order_id, product_id, product_name, quantity, unit_price) '
                                   'VALUES(?,?,?,?,?)', (order_id, item.flower.id, item.flower.name, item.quantity, item.flower.price))
                connection.execute('UPDATE products SET stock = stock - ? WHERE id=?',
                                   (item.quantity, item.flower.id))
        return order_id

    def list_orders(self):
        with self._connection() as connection:
            return connection.execute('SELECT id, customer, created_at, total FROM orders ORDER BY id DESC').fetchall()
