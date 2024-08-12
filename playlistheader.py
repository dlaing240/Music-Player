import tkinter as tk

from listheader import ListHeader
from createplaylistbutton import CreatePlaylistButton


class PlaylistsHeader(ListHeader):
    """Class for the header for the list of playlists."""
    def __init__(self, parent, create_playlist_command):
        """Initialise the `PlaylistsHeader` instance."""
        super().__init__(parent, list_title="Playlists")

        self.button = CreatePlaylistButton(self, create_playlist_command)
        self.button.grid(row=1, column=0)
