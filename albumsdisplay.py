from functools import partial

from albumitem import AlbumItem
from musicdatabase import MusicDatabase


class AlbumsDisplay:
    """
    Class to display the list of albums.

    Attributes
    ----------
    albums_items_dict : dict
        Dictionary where the keys are `album_id`s and the values are
        the `AlbumItem`s created to represent that album.

    Methods
    -------
    display_album_list():
        Displays the list of all albums in the database.
    clear_display():
        Removes all widgets on the current display.
    """

    def __init__(self, display_frame, display_canvas,
                 music_database: MusicDatabase, open_album_command):
        """
        Initialise an `AlbumsDisplay` instance.

        Parameters
        ----------
        display_frame : tkinter.Frame
            The frame to place widgets upon.
        display_canvas : tkinter.Canvas
            The scrollable canvas that contains the `display_frame`.
        music_database : MusicDatabase
            Instance of the Music Database class.
        open_album_command : callable
            Method called when an 'open' button is pressed.
        """
        self._display_frame = display_frame
        self._display_canvas = display_canvas
        self._music_database = music_database
        self._open_album_command = open_album_command

        self.albums_items_dict = {}

    def display_album_list(self):
        """Displays the list of all albums in the database."""
        self.clear_display()

        album_list = self._music_database.get_all_albums()
        albums_info = self._music_database.get_album_metadata(album_list)
        for album in album_list:
            info = albums_info[album]
            self._create_album_item(album, info)

        # Move to the top of the scrollable canvas
        self._display_canvas.yview_moveto(0)

    def _create_album_item(self, album_id, album_info):
        """Creates an instance of the `AlbumItems` class for a given album."""
        album_name = album_info["album_name"]
        artist_id = album_info["artist_id"]
        artist_name = album_info["artist_name"]
        release_date = album_info["release_date"]
        open_album_command = partial(self._open_album_command,
                                     album_id, album_name)

        album = AlbumItem(
            self._display_frame,
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
        """Removes all widgets on the current display."""
        for artist_item_id in self.albums_items_dict:
            self.albums_items_dict[artist_item_id].destroy()

        self.albums_items_dict = {}
