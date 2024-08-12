import tkinter as tk

from root import colour_scheme


class NowPlayingInfo(tk.Frame):
    """
    Class to display information on the current track.

    Methods
    -------
    update_now_playing(track_title, artist_name, album):
        Update the displayed information.
    """

    def __init__(self, parent):
        """Initialise a `NowPlayingInfo` instance."""
        super().__init__(parent)
        self._colour_scheme = colour_scheme

        self.config(bg=self._colour_scheme["dark"])

        self._label = tk.Label(self, text="Now Playing:",
                               font=("Arial", 14),
                               bg=self._colour_scheme["dark"],
                               fg=self._colour_scheme["yellow"])
        self._label.grid(row=0, column=0, padx=10)

        self._track_label = tk.Label(self, text="Track",
                                     font=("Arial", 12),
                                     bg=self._colour_scheme["dark"],
                                     fg="white")
        self._track_label.grid(row=1, column=0, pady=5)

        self._info_label = tk.Label(self, text="Artist - Album",
                                    font=("Arial", 12),
                                    bg=self._colour_scheme["dark"],
                                    fg="white")
        self._info_label.grid(row=2, column=0)

        self._grid_config()

    def _grid_config(self):
        """Configure the way the grid expands."""
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def update_now_playing(self, track_title, artist_name, album):
        """Update the displayed information."""
        self._track_label.config(text=track_title)
        self._info_label.config(text=f"{artist_name} - {album}")
