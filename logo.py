import tkinter as tk

from root import colour_scheme


class Logo(tk.Frame):
    """Class for the application's logo"""

    def __init__(self, parent):
        """Initialise the `Logo` instance."""
        super().__init__(parent)
        self._colour_scheme = colour_scheme
        self.configure(bg=self._colour_scheme["grey"])
        label = tk.Label(self, text="Music Player",
                         bg=self._colour_scheme["grey"],
                         fg=self._colour_scheme["munsell"], font=("Arial", 18))
        label.grid(row=0, column=0, sticky="s")
        logo = tk.Label(self, text="🎹",
                        bg=self._colour_scheme["grey"],
                        fg=self._colour_scheme["munsell"], font=("Arial", 50))
        logo.grid(row=1, column=0, sticky="n")
        self._grid_config()

    def _grid_config(self):
        """Configure the expansion of the grid."""
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
