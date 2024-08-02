import tkinter as tk

from root import colour_scheme, BUTTON_COL


PLAY_BAR_COL = colour_scheme["dark"]


class NowPlayingInfo(tk.Frame):
    """
    Class to display information on the current track
    """
    def __init__(self, parent, track_title, artist_name, album):
        super().__init__(parent)

        self.track_title = track_title
        self.artist_name = artist_name
        self.album = album

        self.config(bg=PLAY_BAR_COL)

        self.label = tk.Label(self, text="Now Playing:", font=("Arial", 14), bg=PLAY_BAR_COL, fg=BUTTON_COL)
        self.label.grid(row=0, column=0, padx=10)

        self.track_label = tk.Label(self, text="Track", font=("Arial", 12), bg=PLAY_BAR_COL, fg="white", width=21)
        self.track_label.grid(row=1, column=0, pady=5)

        self.info_label = tk.Label(self, text="Artist - Album", font=("Arial", 12), bg=PLAY_BAR_COL, fg="white")
        self.info_label.grid(row=2, column=0)

        self._grid_config()

    def _grid_config(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def update_now_playing(self, track_title, artist_name, album):
        """
        Updates the displayed information
        """
        self.track_label.config(text=track_title)
        self.info_label.config(text=f"{artist_name} - {album}")
