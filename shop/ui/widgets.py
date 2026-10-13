"""Небольшие компоненты интерфейса магазина."""
import tkinter as tk
from tkinter import ttk

BG = '#f8f6f3'
PAPER = '#ffffff'
INK = '#29362c'
MUTED = '#788177'
GREEN = '#446653'
PALE = '#e9efe9'
BORDER = '#e5e8e3'


class ShopFrame(tk.Frame):
    def __init__(self, master, **kwargs):
        kwargs.setdefault('bg', BG)
        super().__init__(master, **kwargs)


class PaperFrame(tk.Frame):
    def __init__(self, master, **kwargs):
        kwargs.setdefault('bg', PAPER)
        kwargs.setdefault('highlightbackground', BORDER)
        kwargs.setdefault('highlightthickness', 1)
        super().__init__(master, **kwargs)


class TitleLabel(tk.Label):
    def __init__(self, master, **kwargs):
        kwargs.setdefault('bg', BG)
        kwargs.setdefault('fg', INK)
        kwargs.setdefault('font', ('Segoe UI', 23, 'bold'))
        super().__init__(master, **kwargs)


class SectionLabel(tk.Label):
    def __init__(self, master, **kwargs):
        kwargs.setdefault('bg', PAPER)
        kwargs.setdefault('fg', INK)
        kwargs.setdefault('font', ('Segoe UI', 12, 'bold'))
        super().__init__(master, **kwargs)


class HintLabel(tk.Label):
    def __init__(self, master, **kwargs):
        kwargs.setdefault('bg', PAPER)
        kwargs.setdefault('fg', MUTED)
        kwargs.setdefault('font', ('Segoe UI', 10))
        super().__init__(master, **kwargs)


class PrimaryButton(tk.Button):
    def __init__(self, master, **kwargs):
        kwargs.setdefault('bg', GREEN)
        kwargs.setdefault('fg', 'white')
        kwargs.setdefault('activebackground', '#31513e')
        kwargs.setdefault('activeforeground', 'white')
        kwargs.setdefault('relief', 'flat')
        kwargs.setdefault('cursor', 'hand2')
        kwargs.setdefault('font', ('Segoe UI', 10, 'bold'))
        kwargs.setdefault('padx', 16)
        kwargs.setdefault('pady', 9)
        super().__init__(master, **kwargs)


class SecondaryButton(tk.Button):
    def __init__(self, master, **kwargs):
        kwargs.setdefault('bg', PALE)
        kwargs.setdefault('fg', INK)
        kwargs.setdefault('activebackground', '#dbe4da')
        kwargs.setdefault('relief', 'flat')
        kwargs.setdefault('cursor', 'hand2')
        kwargs.setdefault('font', ('Segoe UI', 10))
        kwargs.setdefault('padx', 12)
        kwargs.setdefault('pady', 8)
        super().__init__(master, **kwargs)


class ShopEntry(tk.Entry):
    def __init__(self, master, **kwargs):
        kwargs.setdefault('bg', PAPER)
        kwargs.setdefault('fg', INK)
        kwargs.setdefault('relief', 'solid')
        kwargs.setdefault('bd', 1)
        kwargs.setdefault('font', ('Segoe UI', 11))
        super().__init__(master, **kwargs)


class ShopSpinbox(tk.Spinbox):
    def __init__(self, master, **kwargs):
        kwargs.setdefault('from_', 1)
        kwargs.setdefault('to', 999)
        kwargs.setdefault('width', 4)
        kwargs.setdefault('font', ('Segoe UI', 11))
        kwargs.setdefault('relief', 'solid')
        kwargs.setdefault('bd', 1)
        super().__init__(master, **kwargs)


class ShopCombobox(ttk.Combobox):
    def __init__(self, master, **kwargs):
        kwargs.setdefault('state', 'readonly')
        kwargs.setdefault('font', ('Segoe UI', 10))
        super().__init__(master, **kwargs)


class ShopTreeview(ttk.Treeview):
    def __init__(self, master, **kwargs):
        kwargs.setdefault('show', 'headings')
        kwargs.setdefault('selectmode', 'browse')
        super().__init__(master, **kwargs)


class ShopSeparator(ttk.Separator):
    def __init__(self, master, **kwargs):
        kwargs.setdefault('orient', 'horizontal')
        super().__init__(master, **kwargs)
