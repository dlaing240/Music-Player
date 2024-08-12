import tkinter as tk

from root import colour_scheme


class ListHeader(tk.Frame):
    """Class for the header of lists of collections."""

    def __init__(self, parent, list_title):
        """
        Initialise a `ListHeader` instance.

        Parameters
        ----------
        parent : tkinter widget
            The parent widget of this frame.
        list_title : str
            The title of the list. ("Albums", "Artists", "Playlists")
        """
        super().__init__(parent)
        self._list_title = list_title
        self._parent = parent
        self._colour_scheme = colour_scheme

        self.padding_size = self._parent.padding_size
        self.config(width=640 - self.padding_size * 2,
                    height=100 - self.padding_size * 2, bg=self._colour_scheme["grey"])
        self._grid_config()

        self._create_widgets()

    def _grid_config(self):
        """Configure the way the grid expands."""
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

    def _create_widgets(self):
        """Create the widgets for the header"""
        header_text = tk.Label(self, text=self._list_title,
                               bg=self._colour_scheme["grey"], fg="White", font=("Arial", 40))
        header_text.grid(row=0, column=0, columnspan=3, padx=10, sticky="ws")
