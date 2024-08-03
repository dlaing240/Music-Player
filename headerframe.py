import tkinter as tk

from root import Root, colour_scheme


HEADER_COL = colour_scheme["grey"]


class HeaderFrame(tk.Frame):
    """
    Class to provide the header for the application
    """
    def __init__(self, parent: Root):
        super().__init__()

        self.parent = parent
        self.padding_size = self.parent.padding_size
        self.grid(row=0, column=1, sticky="news", padx=self.padding_size, pady=self.padding_size)
        self.config(width=640 - self.padding_size*2, height=100 - self.padding_size*2, bg=HEADER_COL)