from functools import partial

from artistitem import ArtistItem
from musicdatabase import MusicDatabase


class ArtistsDisplay:
    """
    Class for displaying the list of artists.

    Attributes
    ----------
    artists_items_dict : dict
        Dictionary with `artist_id` keys and `ArtistItem` values.

    Methods
    -------
    display_artist_list():
        Display a list of all artists in the database.
    clear_display():
        Remove all widgets on the current display.

    """

    def __init__(self, display_frame, display_canvas,
                 music_database: MusicDatabase, open_artist_command):
        """
        Initialise an `ArtistsDisplay` instance.

        Parameters
        ----------
        display_frame : tkinter.Frame
            The frame to place widgets upon.
        display_canvas : tkinter.Canvas
            The scrollable canvas that contains the `display_frame`.
        music_database : MusicDatabase
            Instance of the Music Database class.
        open_artist_command : callable
            Method called when an 'open' button is pressed.
        """
        self._display_frame = display_frame
        self._display_canvas = display_canvas
        self._music_database = music_database
        self._open_artist_command = open_artist_command

        self.artists_items_dict = {}

    def display_artist_list(self):
        """Display a list of all artists in the database."""
        self.clear_display()

        artist_list = self._music_database.get_all_artists()
        artist_info = self._music_database.get_artist_metadata(artist_list)

        for artist_id in artist_list:
            info = artist_info[artist_id]
            self._create_artist_item(artist_id, info)

        # Move to the top of the scrollable canvas.
        self._display_canvas.yview_moveto(0)

    def _create_artist_item(self, artist_id, artist_info):
        """Create an instance of the ArtistItem class for the given artist"""
        artist_name = artist_info["artist_name"]
        open_artist_page_command = partial(self._open_artist_command,
                                           artist_id)
        artist = ArtistItem(self._display_frame,
                            artist_name, open_artist_page_command)
        artist.grid(column=0, sticky="news", pady=5, padx=10)
        self.artists_items_dict[artist_id] = artist

    def clear_display(self):
        """Remove all widgets on the current display."""
        for artist_item_id in self.artists_items_dict:
            self.artists_items_dict[artist_item_id].destroy()

        self.artists_items_dict = {}
