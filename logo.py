import tkinter as tk

from root import colour_scheme, MUNSELL


class Logo(tk.Frame):
    """
    Class for the application's logo display
    """
    def __init__(self, parent):
        super().__init__(parent)

        self.configure(bg=colour_scheme["grey"])
        label = tk.Label(self, text="Music Player", bg=colour_scheme["grey"], fg=MUNSELL, font=("Arial", 18))
        label.grid(row=0, column=0, sticky="s")
        logo = tk.Label(self, text="🎹🪗", bg=colour_scheme["grey"], fg=MUNSELL, font=("Arial", 50))
        logo.grid(row=1, column=0, sticky="n")
        self._grid_config()

    def _grid_config(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)