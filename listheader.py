import tkinter as tk

from root import colour_scheme, BUTTON_COL
HEADER_COL = colour_scheme["grey"]


class ListHeader(tk.Frame):
    def __init__(self, parent, list_title):
        super().__init__(parent)
        self.list_title = list_title
        self.parent = parent

        self.padding_size = self.parent.padding_size
        self.config(width=640 - self.padding_size * 2,
                    height=100 - self.padding_size * 2, bg=HEADER_COL)
        self._grid_config()

        self.create_widgets()

    def _grid_config(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

    def create_widgets(self):
        header_text = tk.Label(self, text=self.list_title,
                               bg=HEADER_COL, fg="White", font=("Arial", 40))
        header_text.grid(row=0, column=0, columnspan=3, padx=10, sticky="ws")
