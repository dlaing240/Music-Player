import tkinter as tk


colour_scheme = {
        "name": "Light 1",
        "grey": "#333533",
        "background": "#E8EDDF",
        "yellow": "#F5CB5C",
        "markers2": "#2B59C3",
        "markers3": "#D36582",
        "dark": "#242524"
    }

# #007C77 - Skobeloff
# #E6AACE - Lavendar pink
# #0CCE6B - Emerald
# #40F99B - Spring green
# #E3170A - Chili Red

MUNSELL = "#468C98"
EMERALD = "#0CCE6B"
CHILI_RED = "#E3170A"
BATTLESHIP_GREY = "#828E82"
DOGWOOD = "#D90368"

# BUTTON_COL = "#3F88C5"
BUTTON_COL = colour_scheme["yellow"]
#BUTTON_COL = CHILI_RED
# BUTTON_COL = DOGWOOD
# BUTTON_COL = EMERALD


class Root(tk.Tk):
    def __init__(self):
        super().__init__()
        self.minsize(width=800, height=600)
        self.config(bg=colour_scheme["grey"])
        # Allow rows and columns to expand when the window is resized
        self._configure_row_and_cols()
        self.padding_size = 2
        self.title("Music Player")

    def _configure_row_and_cols(self):
        self.grid_rowconfigure(0, weight=3)
        self.grid_rowconfigure(1, weight=6)
        self.grid_rowconfigure(2, weight=2)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=6)
