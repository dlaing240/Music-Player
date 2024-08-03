import tkinter as tk

from root import Root
from tracklist import TrackList

from root import colour_scheme


# HEADER_COL = "#F6F7EB"
# SIDE_BAR_COL = "#F6F7EB"


SIDE_BAR_COL = colour_scheme["grey"]


class SideBarFrame(tk.Frame):
    """
    Class to provide the navigation sidebar for the application
    """
    def __init__(self, parent: Root, track_list: TrackList):
        super().__init__()

        self.parent = parent
        self.track_list = track_list

        self.padding_size = self.parent.padding_size
        self.grid(row=1, column=0, rowspan=1, sticky="news", padx=self.padding_size, pady=self.padding_size)
        self.config(width=60 - self.padding_size*2, height=150 - self.padding_size*2, bg=SIDE_BAR_COL)

        self._create_nav_buttons()

        self.open_song_list_observers = [track_list]
        self.open_album_list_observers = []
        self.open_artist_list_observers = []

        self._grid_config()

    def _grid_config(self):
        self.grid_columnconfigure(0, weight=1)

    def _create_nav_buttons(self):
        tk.Button(self, text="⏭️ Up Next", font=("Ariel", 16), command=self.send_open_song_list_signal, width=10,
                  fg="white", bg=colour_scheme["grey"], highlightthickness=0, relief="flat", anchor="w").grid(row=0,
                                                                                                              column=0,
                                                                                                              padx=10,
                                                                                                              pady=5)
        tk.Button(self, text="🎵 Songs", font=("Ariel", 16), command=self.send_open_song_list_signal, width=10, fg="white", bg=colour_scheme["grey"], highlightthickness=0, relief="flat", anchor="w").grid(row=1, column=0, padx=10, pady=5)
        tk.Button(self, text="💿 Albums", font=("Ariel", 16), command=self.send_open_album_list_signal, width=10, fg="white", bg=colour_scheme["grey"], highlightthickness=0, relief="flat", anchor="w").grid(row=2, column=0, padx=10, pady=5)
        tk.Button(self, text="👤 Artists", font=("Ariel", 16), command=self.send_open_artist_list_signal, width=10, fg="white", bg=colour_scheme["grey"], highlightthickness=0, relief="flat", anchor="w").grid(row=3, column=0, padx=10, pady=5)
        tk.Button(self, text="📂 Playlists", font=("Ariel", 16), command=self.send_open_playlist_signal, width=10, fg="white", bg=colour_scheme["grey"], highlightthickness=0, relief="flat", anchor="w").grid(row=4, column=0, padx=10, pady=5)

    def send_open_playlist_signal(self):
        """
        Signals to any observers that the 'playlists' button has been pressed
        """
        print("Open playlist list")

    def send_open_song_list_signal(self):
        """
        Signals to any observers that the 'songs' button has been pressed
        """

        for observer in self.open_song_list_observers:
            observer.received_open_song_list_signal()

    def send_open_album_list_signal(self):
        """
        Signals to any observers that the 'albums' button has been pressed
        """

        for observer in self.open_album_list_observers:
            observer.received_open_album_list_signal()

    def send_open_artist_list_signal(self):
        """
        Signals to any observers that the 'artists' button has been pressed
        """

        for observer in self.open_artist_list_observers:
            observer.received_open_artist_list_signal()


