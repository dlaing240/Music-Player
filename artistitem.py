import tkinter as tk

from root import colour_scheme, BUTTON_COL


class ArtistItem(tk.Frame):
    """
    Class for objects representing artists in the display
    """
    def __init__(self, parent, artist_name, command):
        super().__init__(parent)
        self.artist_name = artist_name
        self.command = command

        self._create_widgets()
        self.configure(bg=colour_scheme["dark"])

    def _create_widgets(self):
        tk.Label(
            self,
            text=self.artist_name,
            bg=colour_scheme["dark"],
            fg=colour_scheme["background"],
            font=("Arial", 12),
            anchor='w',
            height=2
        ).grid(
            row=0,
            column=1,
            padx=10,
            sticky='w'
        )
        tk.Button(
            self,
            text="Open",
            bg=BUTTON_COL,
            command=self.command
        ).grid(
            row=0,
            column=0,
            padx=20
        )
