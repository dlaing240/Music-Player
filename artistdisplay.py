from functools import partial

from artistitem import ArtistItem
from musicdatabase import MusicDatabase


class ArtistsDisplay:
    def __init__(self, display_frame, display_canvas,
                 music_database: MusicDatabase, open_artist_command):
        self.display_frame = display_frame
        self.display_canvas = display_canvas
        self.music_database = music_database
        self.open_artist_command = open_artist_command

        self.artists_items_dict = {}

    def display_artist_list(self):
        """
        Displays a list of all artists in the database
        """
        self.clear_display()

        artist_list = self.music_database.get_all_artists()
        artist_info = self.music_database.get_artist_metadata(artist_list)

        for artist_id in artist_list:
            info = artist_info[artist_id]
            self.create_artist_item(artist_id, info)

        # Move to the top of the scrollable canvas.
        self.display_canvas.yview_moveto(0)

    def create_artist_item(self, artist_id, artist_info):
        """
        Creates an instance of the ArtistItem class for the given artist
        """
        artist_name = artist_info["artist_name"]
        open_artist_page_command = partial(self.open_artist_command,
                                           artist_id)
        artist = ArtistItem(self.display_frame,
                            artist_name, open_artist_page_command)
        artist.grid(column=0, sticky="news", pady=5, padx=10)
        self.artists_items_dict[artist_id] = artist

    def clear_display(self):
        """
        Removes all widgets on the current display
        """
        for artist_item_id in self.artists_items_dict:
            self.artists_items_dict[artist_item_id].destroy()

        self.artists_items_dict = {}
