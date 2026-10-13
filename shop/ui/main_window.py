import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from shop.ui.widgets import (
    BG, PAPER, INK, MUTED, GREEN, BORDER, ShopFrame, PaperFrame,
    TitleLabel, SectionLabel, HintLabel, PrimaryButton, SecondaryButton,
    ShopEntry, ShopSpinbox, ShopCombobox, ShopTreeview, ShopSeparator,
)


class MainWindow(tk.Tk):
    def __init__(self, service, session):
        super().__init__()
        self.service = service
        self.session = session
        self.title('Floré — цветочная мастерская')
        self.geometry('1180x760')
        self.minsize(1010, 650)
        self.configure(bg=BG)
        self.protocol('WM_DELETE_WINDOW', self.close_window)
        self._set_styles()
        self._build_layout()
        self.refresh()

    def _set_styles(self):
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('Treeview', background=PAPER, fieldbackground=PAPER,
                        foreground=INK, rowheight=38, borderwidth=0, font=('Segoe UI', 10))
        style.configure('Treeview.Heading', background='#eef2eb', foreground=GREEN,
                        padding=12, font=('Segoe UI', 10, 'bold'), relief='flat')
        style.map('Treeview', background=[('selected', '#d9e7d9')], foreground=[('selected', INK)])
        style.configure('TCombobox', padding=5)

    def _build_layout(self):
        header = tk.Frame(self, bg=GREEN, height=85)
        header.pack(fill='x')
        header.pack_propagate(False)
        tk.Label(header, text='FLORÉ', font=('Georgia', 26, 'bold'), bg=GREEN, fg='white').pack(side='left', padx=36, pady=19)
        tk.Label(header, text='цветочная мастерская  •  учёт заказов', font=('Segoe UI', 11),
                 bg=GREEN, fg='#dce9dd').pack(side='left', padx=12)
        tk.Label(header, text='КАССА И КАТАЛОГ', font=('Segoe UI', 10, 'bold'),
                 bg=GREEN, fg='#dce9dd').pack(side='right', padx=38)

        outer = ShopFrame(self)
        outer.pack(fill='both', expand=True, padx=30, pady=22)
        top = ShopFrame(outer)
        top.pack(fill='x', pady=(0, 16))
        TitleLabel(top, text='Каталог цветов').pack(side='left')
        self.stats = tk.Label(top, bg=BG, fg=MUTED, font=('Segoe UI', 10))
        self.stats.pack(side='right', pady=10)

        body = ShopFrame(outer)
        body.pack(fill='both', expand=True)
        body.columnconfigure(0, weight=3)
        body.columnconfigure(1, weight=2)
        body.rowconfigure(0, weight=1)

        left = PaperFrame(body)
        left.grid(row=0, column=0, sticky='nsew', padx=(0, 14))
        right = PaperFrame(body)
        right.grid(row=0, column=1, sticky='nsew')
        self._build_catalog(left)
        self._build_cart(right)

    def _build_catalog(self, parent):
        top = tk.Frame(parent, bg=PAPER)
        top.pack(fill='x', padx=20, pady=(22, 14))
        SectionLabel(top, text='Цветы и букеты').pack(side='left')
        self.search_var = tk.StringVar()
        self.search_var.trace_add('write', lambda *_: self.refresh_catalog())
        search_row = tk.Frame(parent, bg=PAPER)
        search_row.pack(fill='x', padx=20, pady=(0, 15))
        ShopEntry(search_row, textvariable=self.search_var, width=26).pack(side='left', fill='x', expand=True, ipady=6)
        self.category = ShopCombobox(search_row, values=('Все', 'Цветы', 'Букеты'), width=12)
        self.category.set('Все')
        self.category.pack(side='left', padx=(8, 0))
        self.category.bind('<<ComboboxSelected>>', lambda *_: self.refresh_catalog())
        self.sort_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(parent, text='Сначала недорогие', variable=self.sort_var,
                        command=self.refresh_catalog).pack(anchor='w', padx=20, pady=(0, 12))

        table_frame = tk.Frame(parent, bg=PAPER)
        table_frame.pack(fill='both', expand=True, padx=20)
        self.products = ShopTreeview(table_frame, columns=('name', 'category', 'price', 'stock'))
        for key, name, width, anchor in (
            ('name', 'Название', 190, 'w'), ('category', 'Категория', 90, 'w'),
            ('price', 'Цена', 85, 'e'), ('stock', 'Остаток', 80, 'center')):
            self.products.heading(key, text=name)
            self.products.column(key, width=width, anchor=anchor, minwidth=70)
        scroll = ttk.Scrollbar(table_frame, orient='vertical', command=self.products.yview)
        self.products.configure(yscrollcommand=scroll.set)
        self.products.pack(side='left', fill='both', expand=True)
        scroll.pack(side='right', fill='y')

        controls = tk.Frame(parent, bg=PAPER)
        controls.pack(fill='x', padx=20, pady=17)
        HintLabel(controls, text='Количество').pack(side='left', padx=(0, 10))
        self.quantity = ShopSpinbox(controls)
        self.quantity.pack(side='left', ipady=6)
        PrimaryButton(controls, text='Добавить в заказ', command=self.add_item).pack(side='right')
        SecondaryButton(controls, text='Изменить остаток', command=self.edit_stock).pack(side='right', padx=8)

    def _build_cart(self, parent):
        SectionLabel(parent, text='Текущий заказ').pack(anchor='w', padx=20, pady=(22, 6))
        HintLabel(parent, text='Выберите цветы слева и добавьте их в заказ').pack(anchor='w', padx=20, pady=(0, 16))
        ShopSeparator(parent).pack(fill='x', padx=20, pady=(0, 10))
        table_frame = tk.Frame(parent, bg=PAPER)
        table_frame.pack(fill='both', expand=True, padx=20)
        self.cart = ShopTreeview(table_frame, columns=('name', 'quantity', 'amount'))
        for key, title, width, anchor in (
            ('name', 'Товар', 175, 'w'), ('quantity', 'Кол-во', 65, 'center'),
            ('amount', 'Сумма', 95, 'e')):
            self.cart.heading(key, text=title)
            self.cart.column(key, width=width, anchor=anchor, minwidth=60)
        self.cart.pack(fill='both', expand=True)
        SecondaryButton(parent, text='Убрать выбранный товар', command=self.remove_item).pack(anchor='e', padx=20, pady=12)
        ShopSeparator(parent).pack(fill='x', padx=20, pady=(0, 16))
        row = tk.Frame(parent, bg=PAPER)
        row.pack(fill='x', padx=20)
        SectionLabel(row, text='Итого').pack(side='left')
        self.total_label = tk.Label(row, text='0 ₽', bg=PAPER, fg=GREEN, font=('Segoe UI', 20, 'bold'))
        self.total_label.pack(side='right')
        HintLabel(parent, text='Покупатель').pack(anchor='w', padx=20, pady=(22, 5))
        self.customer = ShopEntry(parent)
        self.customer.pack(fill='x', padx=20, ipady=8)
        PrimaryButton(parent, text='Оформить заказ', command=self.checkout).pack(fill='x', padx=20, pady=(14, 14))
        SecondaryButton(parent, text='История заказов', command=self.show_orders).pack(fill='x', padx=20, pady=(0, 20))

    def refresh_catalog(self):
        previous = self.products.selection()
        self.products.delete(*self.products.get_children())
        for flower in self.service.filtered_products(self.search_var.get(), self.category.get(), self.sort_var.get()):
            self.products.insert('', 'end', iid=str(flower.id),
                                 values=(flower.name, flower.category, f'{flower.price:,.0f} ₽', flower.stock))
        if previous and self.products.exists(previous[0]):
            self.products.selection_set(previous[0])

    def refresh_cart(self):
        self.cart.delete(*self.cart.get_children())
        for item in self.service.basket:
            self.cart.insert('', 'end', iid=str(item.flower.id),
                             values=(item.flower.name, item.quantity, f'{item.amount:,.0f} ₽'))
        self.total_label.configure(text=f'{self.service.basket_total:,.0f} ₽')

    def refresh(self):
        self.refresh_catalog()
        self.refresh_cart()
        self.stats.configure(text=f'{len(self.service.catalog)} товаров в каталоге')

    def _selected_id(self, tree):
        selected = tree.selection()
        if not selected:
            raise ValueError('Сначала выберите товар')
        return int(selected[0])

    def add_item(self):
        try:
            self.service.add_to_basket(self._selected_id(self.products), int(self.quantity.get()))
            self.refresh_cart()
        except (ValueError, tk.TclError) as exc:
            messagebox.showwarning('Проверьте данные', str(exc), parent=self)

    def remove_item(self):
        try:
            self.service.remove_from_basket(self._selected_id(self.cart))
            self.refresh_cart()
        except ValueError as exc:
            messagebox.showwarning('Выберите товар', str(exc), parent=self)

    def checkout(self):
        try:
            number = self.service.checkout(self.customer.get())
            self.customer.delete(0, 'end')
            self.refresh()
            messagebox.showinfo('Заказ оформлен', f'Заказ №{number} сохранён', parent=self)
        except ValueError as exc:
            messagebox.showwarning('Невозможно оформить заказ', str(exc), parent=self)

    def edit_stock(self):
        try:
            product_id = self._selected_id(self.products)
            product = self.service.catalog.find(product_id)
            new_stock = simpledialog.askinteger('Остаток на складе', product.name,
                                                initialvalue=product.stock, minvalue=0, parent=self)
            if new_stock is not None:
                self.service.change_stock(product_id, new_stock)
                self.refresh_catalog()
        except ValueError as exc:
            messagebox.showwarning('Выберите товар', str(exc), parent=self)

    def show_orders(self):
        window = tk.Toplevel(self)
        window.title('История заказов')
        window.geometry('650x420')
        window.configure(bg=BG)
        TitleLabel(window, text='История заказов').pack(anchor='w', padx=20, pady=18)
        table = ShopTreeview(window, columns=('id', 'customer', 'date', 'total'))
        for key, title, width in (('id', '№', 55), ('customer', 'Покупатель', 180),
                                  ('date', 'Дата', 170), ('total', 'Сумма', 110)):
            table.heading(key, text=title)
            table.column(key, width=width)
        for row in self.service.repository.list_orders():
            table.insert('', 'end', values=(row[0], row[1], row[2], f'{row[3]:,.0f} ₽'))
        table.pack(fill='both', expand=True, padx=20, pady=(0, 20))

    def close_window(self):
        try:
            self.session.finish()
        finally:
            self.destroy()
