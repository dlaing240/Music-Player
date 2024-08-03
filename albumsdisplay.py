import tkinter as tk
from functools import partial

from albumitem import AlbumItem
from musicdatabase import MusicDatabase


class AlbumsDisplay:
    def __init__(self, display_frame, display_canvas, music_database: MusicDatabase, open_album_command):
        self.display_frame = display_frame
        self.display_canvas = display_canvas
        self.music_database = music_database
        self.open_album_command = open_album_command

        self.albums_items_dict = {}

    def display_album_list(self):
        """
        Displays a list of all albums
        """
        self.clear_display()

        album_list = self.music_database.get_all_albums()
        albums_info = self.music_database.get_album_metadata(album_list)
        for album in album_list:
            info = albums_info[album]
            self.create_album_item(album, info)

        self.display_canvas.yview_moveto(0)  # Moves to the top of the scrollable canvas.

    def create_album_item(self, album_id, album_info):
        """
        Creates an instance of the AlbumItems class for a given album
        """
        album_name = album_info["album_name"]
        artist_id = album_info["artist_id"]
        artist_name = album_info["artist_name"]
        release_date = album_info["release_date"]
        open_album_command = partial(self.open_album_command, album_id, album_name)

        album = AlbumItem(
            self.display_frame,
            album_id=album_id,
            album_name=album_name,
            artist_id=artist_id,
            artist_name=artist_name,
            release_date=release_date,
            open_album_command=open_album_command
        )
        album.grid(column=0, sticky="news", pady=5, padx=10)

        self.albums_items_dict[album_id] = album

    def clear_display(self):
        """
        Removes all widgets on the current display
        """
        for artist_item_id in self.albums_items_dict:
            self.albums_items_dict[artist_item_id].destroy()

        self.albums_items_dict = {}

