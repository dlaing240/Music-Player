import tkinter as tk

from root import Root
from tracklist import TrackList

from root import colour_scheme


class SideBarFrame(tk.Frame):
    """
    Class to provide the navigation sidebar for the application.

    Attributes
    ----------
    open_song_list_observers : list
        List of observers with the `received_open_song_list_signal()`
        method.
    open_album_list_observers : list
        List of observers with the `received_open_album_list_signal()`
        method.
    open_artist_list_observers : list
        List of observers with the `received_open_artist_list_signal()`
        method.
    open_queue_observers : list
        List of observers with the `received_open_queue_signal()`
        method.
    open_playlist_observers : list
        List of observers with the `received_open_playlist_signal()`
        method.
    open_directories_observers : list
        List of observers with the `received_open_directories_signal()`
        method.
    """

    def __init__(self, parent: Root, track_list: TrackList):
        """
        Initialise a `SideBarFrame` instance.

        Parameters
        ----------
        parent : Root
            The root window for the application.
        track_list : TrackList
            Instance of `TrackList`.
        """
        super().__init__()

        self.parent = parent
        self._track_list = track_list
        self._colour_scheme = colour_scheme

        self.padding_size = self.parent.padding_size
        self.grid(row=1, column=0, rowspan=1, sticky="news",
                  padx=self.padding_size, pady=self.padding_size)
        self.config(width=60 - self.padding_size*2,
                    height=150 - self.padding_size*2, bg=self._colour_scheme["grey"])

        self._create_nav_buttons()

        self.open_song_list_observers = [track_list]
        self.open_album_list_observers = []
        self.open_artist_list_observers = []
        self.open_queue_observers = []
        self.open_playlist_observers = []
        self.open_directories_observers = []

        self._grid_config()

    def _grid_config(self):
        """Configure the way the grid expands."""
        self.grid_columnconfigure(0, weight=1)

    def _create_nav_buttons(self):
        """Create the buttons used for navigation."""
        tk.Button(
            self,
            text="⏭️ Up Next",
            font=("Ariel", 16),
            command=self.send_open_queue_signal,
            width=11,
            fg="white",
            bg=self._colour_scheme["grey"],
            highlightthickness=0,
            relief="flat",
            anchor="w"
        ).grid(row=0, column=0, padx=10, pady=5)
        tk.Button(
            self,
            text="🎵 Songs",
            font=("Ariel", 16),
            command=self.send_open_song_list_signal,
            width=11,
            fg="white",
            bg=self._colour_scheme["grey"],
            highlightthickness=0,
            relief="flat",
            anchor="w"
        ).grid(row=1, column=0, padx=10, pady=5)
        tk.Button(
            self,
            text="💿 Albums",
            font=("Ariel", 16),
            command=self.send_open_album_list_signal,
            width=11,
            fg="white",
            bg=self._colour_scheme["grey"],
            highlightthickness=0,
            relief="flat",
            anchor="w"
        ).grid(row=2, column=0, padx=10, pady=5)
        tk.Button(
            self,
            text="👤 Artists",
            font=("Ariel", 16),
            command=self.send_open_artist_list_signal,
            width=11,
            fg="white",
            bg=self._colour_scheme["grey"],
            highlightthickness=0,
            relief="flat",
            anchor="w"
        ).grid(row=3, column=0, padx=10, pady=5)
        tk.Button(
            self,
            text="📂 Playlists",
            font=("Ariel", 16),
            command=self.send_open_playlists_signal,
            width=11,
            fg="white",
            bg=self._colour_scheme["grey"],
            highlightthickness=0,
            relief="flat",
            anchor="w"
        ).grid(row=4, column=0, padx=10, pady=5)

        tk.Button(
            self,
            text="➕ Add Music",
            font=("Ariel", 16),
            command=self.send_open_directories_signal,
            width=11,
            fg="white",
            bg=self._colour_scheme["grey"],
            highlightthickness=0,
            relief="flat",
            anchor="w"
        ).grid(row=5, column=0, padx=10, pady=5)

    def send_open_playlists_signal(self):
        """Calls the observers' `received_open_playlists_signal()` method."""
        for observer in self.open_playlist_observers:
            observer.received_open_playlists_signal()

    def send_open_song_list_signal(self):
        """Calls the observers' `received_open_song_list_signal()` method."""
        for observer in self.open_song_list_observers:
            observer.received_open_song_list_signal()

    def send_open_album_list_signal(self):
        """Calls the observers' `received_open_album_list_signal()` method."""
        for observer in self.open_album_list_observers:
            observer.received_open_album_list_signal()

    def send_open_artist_list_signal(self):
        """Calls the observers' `received_open_artist_list_signal()` method."""
        for observer in self.open_artist_list_observers:
            observer.received_open_artist_list_signal()

    def send_open_queue_signal(self):
        """Calls the observers' `received_open_queue_signal()` method."""
        for observer in self.open_queue_observers:
            observer.received_open_queue_signal()

    def send_open_directories_signal(self):
        """Calls the observers' `received_open_directories_signal()` method."""
        for observer in self.open_directories_observers:
            observer.received_open_directories_signal()
