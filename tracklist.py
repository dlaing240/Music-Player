from musicdatabase import MusicDatabase


from durationformat import format_duration


class TrackList:
    """
    Class to represent a list of tracks
    """
    def __init__(self, music_database: MusicDatabase):
        self.music_db = music_database  # For interactions with the database

        self.tracklist_updated_observers = []
        self.tracklist = []
        self.has_changed = False

        self.collection_type = None  # Maintains the type of collection being shown (Album, Artist, or all songs)
        self.collection_title = ""  # E.g., Album title, artist name
        self.collection_id = None  # Database ID for the collection

    def get_collection(self, collection_type=None, collection_id=None):
        """
        Gets a list of tracks belonging to a collection, which could
        be an artist's tracks, album, or playlist.

        """
        if not collection_type:
            self.tracklist = self.music_db.get_all_tracks()
            self.collection_type = "all songs"
            self.collection_title = "All Songs"
        elif collection_type == "album":
            self.tracklist = self.music_db.get_album_tracklist(collection_id)
            self.collection_title = self.music_db.get_album_title(collection_id)
            self.collection_type = "album"
        elif collection_type == "artist":
            self.tracklist = self.music_db.get_artist_tracklist(collection_id)
            self.collection_title = self.music_db.get_artist_name(collection_id)
            self.collection_type = "artist"
        elif collection_type == "playlist":
            self.collection_type = "playlist"
            self.collection_title = self.music_db.get_playlist_name(collection_id)
            self.tracklist = self.music_db.get_playlist_tracks(collection_id)
        elif collection_type == "favourites":
            self.collection_type = "favourites"
            self.collection_title = "Favourites"
            pass
        else:
            print("Unrecognised collection type")
            pass

        self.collection_id = collection_id
        self.send_tracklist_updated_signal()

    def send_tracklist_updated_signal(self):
        """
        Sends a signal indicating that the list has been updated to
        any observing objects
        """
        for observer in self.tracklist_updated_observers:
            observer.received_tracklist_updated_signal()

    def received_open_song_list_signal(self):
        """
        Sets the tracklist to contain all tracks in the database
        """
        self.get_collection()

    def received_open_album_signal(self, album_id):
        """
        Sets the tracklist to the tracklist of the provided album
        """
        self.get_collection('album', album_id)

    def received_open_artist_page_signal(self, artist_id):
        """
        Sets the tracklist to the list of songs attributed to the
        provided artist
        """
        self.get_collection('artist', artist_id)

    def received_open_playlist_signal(self, playlist_id):
        self.get_collection('playlist', playlist_id)

    def get_tracklist(self):
        """
        Returns a copy of the current tracklist
        """
        return self.tracklist.copy()

    def get_total_tracklist_duration(self):
        metadata = self.music_db.get_track_metadata(self.tracklist)
        durations = [metadata[track_id]["duration"] for track_id in self.tracklist]
        formatted_duration = format_duration(sum(durations))
        return formatted_duration
