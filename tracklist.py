from musicdatabase import MusicDatabase

from durationformat import format_duration


class TrackList:
    """
    Class to maintain the list of tracks.

    Attributes
    ----------
    tracklist_updated_observers : list
        List of observers with the `received_tracklist_updated_signal()` method.
    tracklist : list
        The current list of `track_id`s.
    has_changed : bool
        True if the tracklist has been changed since the last
        interaction with it. False otherwise.
    collection_type : str
        The type of collection (album, artist, all songs, playlist)
        that the current tracklist represents.
    collection_title : str
        Title of the current collection.
    collection_id : int
        The unique identifier for the collection.

    Methods
    -------
    received_open_song_list_signal():
        Set the tracklist to contain all tracks in the database
    def received_open_album_signal(album_id):
        Set the tracklist to an album
    def received_open_artist_page_signal(artist_id):
        Set the tracklist to an artist's tracks.
    received_open_playlist_signal(playlist_id):
        Set the tracklist to a playlist.
    get_tracklist():
        Return a copy of the current tracklist.
    get_total_tracklist_duration():
        Return the duration of the tracklist in the format 'hh:mm:ss'.

    """

    def __init__(self, music_database: MusicDatabase):
        """
        Initialise a `TrackList` instance.

        Parameters
        ----------
        music_database : MusicDatabase
            Instance of `MusicDatabase`.
        """
        self._music_db = music_database  # For interactions with the database

        self.tracklist_updated_observers = []
        self.tracklist = []
        self.has_changed = False

        self.collection_type = None
        self.collection_title = ""
        self.collection_id = None

    def get_collection(self, collection_type=None, collection_id=None):
        """
        Update `tracklist` to a list of tracks in a certain collection.

        Parameters
        ----------
        collection_type : str, optional
            Type of the collection, "all songs", "album", "artist",
            "playlist". None will default to all songs.
        collection_id : int, optional
            The unique identifier for the collection. If None, the
            collection will be "all songs".
        """
        if not collection_type or collection_type == "all songs" or not collection_id:
            self.tracklist = self._music_db.get_all_tracks()
            self.collection_type = "all songs"
            self.collection_title = "All Songs"
        elif collection_type == "album":
            self.tracklist = self._music_db.get_album_tracklist(collection_id)
            self.collection_title = self._music_db.get_album_title(collection_id)
            self.collection_type = "album"
        elif collection_type == "artist":
            self.tracklist = self._music_db.get_artist_tracklist(collection_id)
            self.collection_title = self._music_db.get_artist_name(collection_id)
            self.collection_type = "artist"
        elif collection_type == "playlist":
            self.collection_type = "playlist"
            self.collection_title = self._music_db.get_playlist_name(collection_id)
            self.tracklist = self._music_db.get_playlist_tracks(collection_id)
        elif collection_type == "favourites":  # Favourites not implemented
            self.collection_type = "favourites"
            self.collection_title = "Favourites"
            pass
        else:
            print("Unrecognised collection type")
            pass

        self.collection_id = collection_id
        self.send_tracklist_updated_signal()

    def send_tracklist_updated_signal(self):
        """Call `received_tracklist_updated_signal()` on observers."""
        self.has_changed = True
        for observer in self.tracklist_updated_observers:
            observer.received_tracklist_updated_signal()

    def received_open_song_list_signal(self):
        """Set the tracklist to contain all tracks in the database"""
        self.get_collection()

    def received_open_album_signal(self, album_id):
        """Set the tracklist to an album"""
        self.get_collection('album', album_id)

    def received_open_artist_page_signal(self, artist_id):
        """Set the tracklist to an artist's tracks."""
        self.get_collection('artist', artist_id)

    def received_open_playlist_signal(self, playlist_id):
        """Set the tracklist to a playlist."""
        self.get_collection('playlist', playlist_id)

    def get_tracklist(self):
        """Return a copy of the current tracklist."""
        return self.tracklist.copy()

    def get_total_tracklist_duration(self):
        """Return the duration of the tracklist in the format 'hh:mm:ss'."""
        metadata = self._music_db.get_track_metadata(self.tracklist)
        durations = [metadata[track_id]["duration"] for track_id in self.tracklist]
        formatted_duration = format_duration(sum(durations))
        return formatted_duration
