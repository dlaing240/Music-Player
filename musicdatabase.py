from artistsdatabase import ArtistsDatabase
from albumsdatabase import AlbumsDatabase
from trackdatabase import TrackDatabase


class MusicDatabase:
    """
    Class which acts as an interface for the database operations classes
    """
    def __init__(self, db_path):
        self.artist_database = ArtistsDatabase(db_path)
        self.albums_database = AlbumsDatabase(db_path, self.artist_database)
        self.tracks_database = TrackDatabase(db_path, self.artist_database, self.albums_database)

    def create_database(self):
        """
        Creates the database tables if they don't already exist
        """
        self.artist_database.create_database()
        self.albums_database.create_database()
        self.tracks_database.create_database()

    def artist_exists(self, artist_name):
        """
        Checks whether the provided artist is in the database
        """
        return self.artist_database.artist_exists(artist_name)

    def insert_artist(self, artist_name):
        """
        Adds the artist to the database
        """
        self.artist_database.insert_artist(artist_name)

    def get_artist_id(self, artist_name):
        """
        Returns the artist's artist_id
        """
        return self.artist_database.get_artist_id(artist_name)

    def get_artist_name(self, artist_id):
        return self.artist_database.get_artist_name(artist_id)

    def get_artist_tracklist(self, artist_id):
        """
        Gets the list of tracks by the provided artist
        """
        return self.artist_database.get_artist_tracklist(artist_id)

    def album_exists(self, album_name, artist, release_date):
        """
        Checks whether the given album can be found in the database
        """
        return self.albums_database.album_exists(album_name, artist, release_date)

    def insert_album(self, album_name, artist, release_date):
        """
        Adds the given album details to the database
        """
        self.albums_database.insert_album(album_name, artist, release_date)

    def get_album_id(self, album_name, release_date):
        """
        Returns an album's album_id
        """
        return self.albums_database.get_album_id(album_name, release_date)

    def get_album_title(self, album_id):  # Redundant? Ideally use get metadata
        return self.albums_database.get_album_title(album_id)

    def get_album_metadata(self, album_ids):
        """
        Method used to get the album data corresponding to the provided album_ids
        """
        return self.albums_database.get_album_metadata(album_ids)

    def get_all_albums(self):
        """
        Method to get a list of all album_ids in the albums database
        """
        return self.albums_database.get_all_albums()

    def get_album_tracklist(self, album_id):
        """
        Method to get the ordered tracklist for an album.
        """
        return self.albums_database.get_album_tracklist(album_id)

    def track_exists(self, file_path):
        """
        Checks whether the file path corresponds to a track in the database
        """
        return self.tracks_database.track_exists(file_path)

    def track_is_duplicate(self, track_name, artist, album, release_date):
        """
        Checks whether the track data matches a track that's already in the database
        """
        return self.tracks_database.track_is_duplicate(track_name, artist, album, release_date)

    def insert_track(self, track_name, artist, album, track_number, release_date, genre, duration, file_path):
        """
        Adds the track to the database
        """
        self.tracks_database.insert_track(track_name, artist, album, track_number, release_date, genre, duration, file_path)

    def get_all_tracks(self):
        """
        Returns a list of all track_ids in the database
        """
        return self.tracks_database.get_all_tracks()

    def get_track_metadata(self, id_list):
        """
        Gets the database data corresponding to the tracks in the list of track_ids.
        """
        return self.tracks_database.get_track_metadata(id_list)

    def get_path(self, track_id):
        """
        Returns the file path of the given track
        """
        return self.tracks_database.get_path(track_id)

    def get_duration(self, track_id):
        """
        Returns the duration of the song
        """
        return self.tracks_database.get_duration(track_id)

    def get_all_artists(self):
        """
        Gets a list of all the artist_ids in the database
        """
        return self.artist_database.get_all_artists()

    def get_artist_metadata(self, artist_ids):
        """
        Gets the database data corresponding to each artist in the given list of artist_ids
        """
        return self.artist_database.get_artist_metadata(artist_ids)
