from tkinter import *
from tkinter import ttk

from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from gui.game_screen import GameScreen


class MainWindow:
    def __init__(self, root: Tk):
        self.root = root
        self.root.title('Breakout!')
        self.root.iconbitmap('gui/arcade_icon.ico')

        mainframe = ttk.Frame(self.root)
        mainframe.grid(column=0, row=0, sticky='nwes')

        canvas = GameScreen(mainframe, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        canvas.grid(column=0, row=0)
