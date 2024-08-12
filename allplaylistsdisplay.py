from functools import partial
import tkinter as tk
from tkinter import messagebox

from musicdatabase import MusicDatabase
from playlistitem import PlaylistItem

from root import colour_scheme


class AllPlaylistsDisplay:
    """
    Class for displaying the list of user playlists.

    Attributes
    ----------
    playlist_items_dict : dict
        Dictionary with `playlist_id` keys and `PlaylistItem` values.

    Methods
    -------
    display_playlist_list():
        Display the list of playlists.
    clear_display():
        Destroy all playlist widgets.
    """

    def __init__(self, display_frame, display_canvas,
                 music_database: MusicDatabase, open_playlist_command):
        """
        Initialise a `AllPlaylistsDisplay` instance.

        Parameters
        ----------
        display_frame : tkinter.Frame
            The frame to place widgets upon.
        display_canvas : tkinter.Canvas
            The scrollable canvas that contains the `display_frame`.
        music_database : MusicDatabase
            Instance of the Music Database class.
        open_playlist_command : callable
            Method called when an 'open' button is pressed.
        """
        self._display_frame = display_frame
        self._display_canvas = display_canvas
        self._music_db = music_database
        self._open_playlist_command = open_playlist_command
        self.playlist_items_dict = {}
        self._colour_scheme = colour_scheme

        self.delete_playlist = self._music_db.delete_playlist

    def display_playlist_list(self):
        """Display the list of playlists."""
        self.clear_display()
        playlists = self._music_db.get_playlists()
        for playlist_id in playlists:
            open_playlist_command = partial(self._open_playlist_command, playlist_id)

            self._create_playlist_item(
                playlist_id,
                playlist_name=playlists[playlist_id],
                open_playlist_command=open_playlist_command
            )

        self._create_delete_buttons()
        self._display_canvas.yview_moveto(0)

    def _create_playlist_item(self, playlist_id, playlist_name,
                              open_playlist_command):
        """Create a playlist item."""
        playlist = PlaylistItem(self._display_frame, open_playlist_command,
                                playlist_id, playlist_name)
        playlist.grid(column=0, sticky="news", pady=5, padx=10)
        self.playlist_items_dict[playlist_id] = playlist

    def _create_delete_buttons(self):
        """Create delete buttons."""
        for playlist_id in self.playlist_items_dict:
            playlist_item = self.playlist_items_dict[playlist_id]

            delete_playlist_command = partial(self._delete_playlist_command,
                                              playlist_id)
            delete_button = tk.Button(playlist_item,
                                      text="❌",
                                      command=delete_playlist_command,
                                      bg=self._colour_scheme["dark"],
                                      fg=self._colour_scheme["chili_red"],
                                      relief="flat",
                                      font=("Arial", 18),
                                      anchor="e")
            delete_button.grid(row=0, column=3,
                               rowspan=2, padx=20,
                               sticky="e")

    def _delete_playlist_command(self, playlist_id):
        """Begin procedure to delete a playlist from the database."""
        response = messagebox.askyesno(
            "Delete Playlist",
            "This will permanently delete the playlist.\nContinue?"
        )
        if response:
            self.delete_playlist(playlist_id)
            self.display_playlist_list()

    def clear_display(self):
        """Destroy all playlist widgets."""
        for playlist_id in self.playlist_items_dict:
            self.playlist_items_dict[playlist_id].destroy()
        self.playlist_items_dict = {}
