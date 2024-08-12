import tkinter as tk

from root import colour_scheme


class PlaylistItem(tk.Frame):
    """Class for widgets that represent playlists in the display."""

    def __init__(self, parent, open_playlist_command, playlist_id,
                 playlist_name):
        """
        Initialise a `PlaylistItem` instance.

        Parameters
        ----------
        parent : tkinter widget.
            The parent widget of this frame.
        open_playlist_command : callable
            The method to open a playlist.
        playlist_id : int
            The identifier of the playlist.
        playlist_name : str
            The title of the playlist.
        """
        super().__init__(parent)
        self._open_playlist_command = open_playlist_command
        self._playlist_id = playlist_id
        self._playlist_name = playlist_name
        self._colour_scheme = colour_scheme

        self._create_widgets()
        self.configure(bg=self._colour_scheme["dark"])

        self.grid_columnconfigure(1, weight=1)

    def _create_widgets(self):
        """Create the `PlaylistItem` widgets."""
        tk.Label(
            self,
            text=self._playlist_name,
            bg=self._colour_scheme["dark"],
            fg=self._colour_scheme["background"],
            font=("Arial", 12),
            anchor='w',
            height=2,
            ).grid(
            row=0,
            column=1,
            rowspan=2,
            padx=10,
            sticky='nesw'
        )
        tk.Button(
            self,
            text="Open",
            bg=self._colour_scheme["yellow"],
            command=self._open_playlist_command
        ).grid(
            row=0,
            column=0,
            rowspan=2,
            padx=20)
