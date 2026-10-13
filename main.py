from pathlib import Path

from shop.repositories.sqlite_repository import SQLiteShopRepository
from shop.services.session_service import SessionService
from shop.services.shop_service import ShopService
from shop.ui.main_window import MainWindow


def main():
    folder = Path(__file__).resolve().parent
    repository = SQLiteShopRepository(folder / 'data' / 'flower_shop.db')
    service = ShopService(repository)
    session = SessionService(folder / 'reports')
    MainWindow(service, session).mainloop()


if __name__ == '__main__':
    main()
