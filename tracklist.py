from musicdatabase import MusicDatabase


class TrackList:
    """
    Class to represent a list of tracks
    """
    def __init__(self, music_database: MusicDatabase):
        self.music_database = music_database  # For interactions with the database

        self.tracklist_updated_observers = []
        self.tracklist = []
        self.has_changed = False

    def get_collection(self, collection_type=None, collection_id=None):
        """
        Gets a list of tracks belonging to a collection, which could be an artist's tracks, album, or playlist.
        """
        if not collection_type:
            self.tracklist = self.music_database.get_all_tracks()
        elif collection_type == "album":
            self.tracklist = self.music_database.get_album_tracklist(collection_id)
        elif collection_type == "artist":
            self.tracklist = self.music_database.get_artist_tracklist(collection_id)
        elif collection_type == "playlist":
            pass
        elif collection_type == "favourites":
            pass
        else:
            print("Unrecognised collection type")
            pass

        self.send_tracklist_updated_signal()

    def send_tracklist_updated_signal(self):
        """
        Sends a signal indicating that the list has been updated to any observing objects
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
        Sets the tracklist to the list of songs attributed to the provided artist
        """
        self.get_collection('artist', artist_id)

    def get_tracklist(self):
        """
        Returns a copy of the current tracklist
        """
        return self.tracklist.copy()

