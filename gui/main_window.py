from tkinter import *
from tkinter import ttk


class MainWindow:
    def __init__(self, root: Tk):
        self.root = root
        self.root.title('Breakout!')
        self.root.iconbitmap('gui/arcade_icon.ico')
