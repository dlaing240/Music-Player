import tkinter as tk

from root import colour_scheme


class ArtistItem(tk.Frame):
    """
    Class for objects representing artists in the display.

    It creates several widgets and places them on a tkinter frame using the grid geometry manager.
    """

    def __init__(self, parent, artist_name, command):
        """
        Initialise an `ArtistItem` instance.

        Parameters
        ----------
        parent : tkinter widget
            The parent widget containing this frame.
        artist_name : str
            The name of the artist.
        command : callable
            The method that is called when the open button is pressed.
        """
        super().__init__(parent)
        self._artist_name = artist_name
        self._command = command
        self._colour_scheme = colour_scheme

        self._create_widgets()
        self.configure(bg=self._colour_scheme["dark"])

    def _create_widgets(self):
        """Create the artist widgets."""
        tk.Label(
            self,
            text=self._artist_name,
            bg=self._colour_scheme["dark"],
            fg=self._colour_scheme["background"],
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
            bg=self._colour_scheme["yellow"],
            command=self._command
        ).grid(
            row=0,
            column=0,
            padx=20
        )
