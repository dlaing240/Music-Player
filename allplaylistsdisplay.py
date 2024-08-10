from functools import partial
import tkinter as tk
from tkinter import messagebox

from musicdatabase import MusicDatabase
from playlistitem import PlaylistItem

from root import colour_scheme, CHILI_RED


class AllPlaylistsDisplay:
    """
    Class for displaying the list of user playlists
    """
    def __init__(self, display_frame, display_canvas,
                 music_database: MusicDatabase, open_playlist_command):
        self.display_frame = display_frame
        self.display_canvas = display_canvas
        self.music_db = music_database
        self.open_playlist_command = open_playlist_command
        self.playlist_items_dict = {}

        self.delete_playlist = self.music_db.delete_playlist

    def display_playlist_list(self):
        """
        Displays the list of playlists

        Returns
        -------

        """
        self.clear_display()
        playlists = self.music_db.get_playlists()
        for playlist_id in playlists:
            open_playlist_command = partial(self.open_playlist_command, playlist_id)

            self.create_playlist_item(
                playlist_id,
                playlist_name=playlists[playlist_id],
                open_playlist_command=open_playlist_command
            )

        self.create_delete_buttons()
        self.display_canvas.yview_moveto(0)

    def create_playlist_item(self, playlist_id, playlist_name,
                             open_playlist_command):
        """
        Creates the playlist item

        Parameters
        ----------
        playlist_id
        playlist_name
        open_playlist_command

        Returns
        -------

        """

        playlist = PlaylistItem(self.display_frame, open_playlist_command,
                                playlist_id, playlist_name)
        playlist.grid(column=0, sticky="news", pady=5, padx=10)
        self.playlist_items_dict[playlist_id] = playlist

    def create_delete_buttons(self):
        for playlist_id in self.playlist_items_dict:
            playlist_item = self.playlist_items_dict[playlist_id]

            delete_playlist_command = partial(self.delete_playlist_command,
                                              playlist_id)
            delete_button = tk.Button(playlist_item,
                                      text="❌",
                                      command=delete_playlist_command,
                                      bg=colour_scheme["dark"],
                                      fg=CHILI_RED,
                                      relief="flat",
                                      font=("Arial", 18),
                                      anchor="e")
            delete_button.grid(row=0, column=3,
                               rowspan=2, padx=20,
                               sticky="e")

    def delete_playlist_command(self, playlist_id):
        response = messagebox.askyesno(
            "Delete Playlist",
            "This will permanently delete the playlist.\nContinue?"
        )
        if response:
            self.delete_playlist(playlist_id)
            self.display_playlist_list()
        else:
            return

    def clear_display(self):
        """
        Destroys all playlist widgets

        Returns
        -------

        """
        for playlist_id in self.playlist_items_dict:
            self.playlist_items_dict[playlist_id].destroy()
        self.playlist_items_dict = {}
