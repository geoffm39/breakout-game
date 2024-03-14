from tkinter import *
from tkinter import ttk

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, TITLE, FilePaths
from gui.game_screen import GameScreen


class MainWindow:
    def __init__(self, root: Tk):
        self.root = root
        self.root.title(TITLE)
        self.root.iconbitmap(FilePaths.ICON)
        self.root.resizable(FALSE, FALSE)

        mainframe = ttk.Frame(self.root)
        mainframe.grid(column=0, row=0, sticky='nwes')

        self.game_screen = GameScreen(mainframe, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        self.game_screen.grid(column=0, row=0)
