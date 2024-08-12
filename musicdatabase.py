from artistsdatabase import ArtistsDatabase
from albumsdatabase import AlbumsDatabase
from trackdatabase import TrackDatabase
from playlistsdatabase import PlaylistDatabase


class MusicDatabase:
    """Class which provides an interface for database operations."""

    def __init__(self, db_path):
        """Initialise a `MusicDatabase` instance."""
        self._artist_database = ArtistsDatabase(db_path)
        self._albums_database = AlbumsDatabase(db_path, self._artist_database)
        self._playlist_database = PlaylistDatabase(db_path)
        self._tracks_database = TrackDatabase(db_path,
                                              self._artist_database,
                                              self._albums_database,
                                              self._playlist_database)
        self.create_database()

    def create_database(self):
        """Create the database tables if they don't already exist."""
        self._artist_database.create_database()
        self._albums_database.create_database()
        self._tracks_database.create_database()
        self._playlist_database.create_tables()

    def artist_exists(self, artist_name):
        """Check if the provided artist is in the database."""
        return self._artist_database.artist_exists(artist_name)

    def insert_artist(self, artist_name):
        """Add an artist to the database."""
        self._artist_database.insert_artist(artist_name)

    def get_artist_id(self, artist_name):
        """Return the artist's `artist_id`."""
        return self._artist_database.get_artist_id(artist_name)

    def get_artist_name(self, artist_id):
        """Get the artist's name from the identifier."""
        return self._artist_database.get_artist_name(artist_id)

    def get_artist_tracklist(self, artist_id):
        """Return the list of tracks by an artist."""
        return self._artist_database.get_artist_tracklist(artist_id)

    def album_exists(self, album_name, artist, release_date):
        """
        Check if an album exists in the database

        The album's title, artist and release date are considered to
        ensure that only exact matches give a positive result.

        Parameters
        ----------
        album_name : str
            The title of the album.
        artist : str
            The name of the artist
        release_date : str
            The release date of the album.

        Returns
        -------
        bool
            `True` if the album exists in the database, `False` otherwise.
        """
        return self._albums_database.album_exists(album_name,
                                                  artist,
                                                  release_date)

    def insert_album(self, album_name, artist, release_date):
        """Insert an album into the database."""
        self._albums_database.insert_album(album_name, artist, release_date)

    def get_album_id(self, album_name, release_date):
        """Return an album's unique identifier."""
        return self._albums_database.get_album_id(album_name, release_date)

    def get_album_title(self, album_id):
        """Return the album's title from its identifier."""
        return self._albums_database.get_album_title(album_id)

    def get_album_metadata(self, album_ids):
        """
        Get data about albums from their identifiers.

        Parameters
        ----------
        album_ids : list of int
            A list containing the unique identifiers of albums in the
            database.

        Returns
        -------
        dict
            A dictionary where each key is an `album_id` and its value
            is a dictionary containing the information about that
            album.
        """
        return self._albums_database.get_album_metadata(album_ids)

    def get_all_albums(self):
        """Return a list of every `album_id` in the albums database."""
        return self._albums_database.get_all_albums()

    def get_album_tracklist(self, album_id):
        """Return a list of `track_id`s in the given album."""
        return self._albums_database.get_album_tracklist(album_id)

    def track_exists(self, file_path):
        """Return True if the file path is in the database and False otherwise."""
        return self._tracks_database.track_exists(file_path)

    def track_is_duplicate(self, track_name, artist, album, release_date):
        """Return True if track is already in the database, False otherwise."""
        return self._tracks_database.track_is_duplicate(track_name, artist,
                                                        album, release_date)

    def insert_track(self, track_name, artist, album, track_number,
                     release_date, genre, duration, file_path):
        """Add a track to the database."""
        self._tracks_database.insert_track(track_name, artist, album,
                                           track_number, release_date,
                                           genre, duration, file_path)

    def get_all_tracks(self):
        """Return a list of all `track_id`s in the database."""
        return self._tracks_database.get_all_tracks()

    def get_track_metadata(self, id_list):
        """
        Return the database data corresponding to the tracks in the list of
        track_ids.

        Returns
        -------
        dict
            A dictionary where keys are `track_id`s and the values are
            dictionaries containing info about that track.
        """
        return self._tracks_database.get_track_metadata(id_list)

    def get_path(self, track_id):
        """Return the file path of the given track."""
        return self._tracks_database.get_path(track_id)

    def get_duration(self, track_id):
        """Return the duration of a track."""
        return self._tracks_database.get_duration(track_id)

    def get_all_artists(self):
        """Return a list of all the artist_ids in the database."""
        return self._artist_database.get_all_artists()

    def get_artist_metadata(self, artist_ids):
        """
        Return data about artists from a list of `artist_id`s.

        Parameters
        ----------
        artist_ids : list
            The `artist_id`s for the artists.

        Returns
        -------
        dict
            Dictionary where the keys are `artist_id`s and the values
            are dictionaries of that artists data.
        """
        return self._artist_database.get_artist_metadata(artist_ids)

    def get_artist_albumlist(self, artist_id):
        """Return a list of albums by the artist."""
        return self._artist_database.get_artist_albumlist(artist_id)

    def create_playlist(self, playlist_name):
        """Create a new playlist with the given name."""
        return self._playlist_database.create_playlist(playlist_name)

    def add_to_playlist(self, track_id, playlist_id):
        """Add a track to a playlist."""
        return self._playlist_database.add_to_playlist(track_id, playlist_id)

    def remove_from_playlist(self, track_id, playlist_id):
        """Remove a track from a playlist."""
        return self._playlist_database.remove_from_playlist(track_id, playlist_id)

    def get_playlist_tracks(self, playlist_id):
        """Return the list of tracks in a playlist."""
        return self._playlist_database.get_playlist_tracks(playlist_id)

    def get_playlists(self):
        """Return a list of all playlists in the database."""
        return self._playlist_database.get_playlists()

    def get_playlist_name(self, playlist_id):
        """Return the name of a playlist from its ID."""
        return self._playlist_database.get_playlist_name(playlist_id)

    def get_all_paths(self):
        """Return a list containing all the file paths in the database."""
        return self._tracks_database.get_all_paths()

    def remove_by_paths(self, file_paths):
        """Remove database entries corresponding to the file paths."""
        return self._tracks_database.remove_by_paths(file_paths)

    def delete_playlist(self, playlist_id):
        """Delete a playlist from the database."""
        return self._playlist_database.delete_playlist(playlist_id)

    def swap_positions(self, playlist_id, pos_1, pos_2):
        """Swap the positions of two tracks in a playlist."""
        return self._playlist_database.swap_positions(playlist_id, pos_1, pos_2)

    def get_track_pos(self, playlist_id, track_id):
        """Return the position of a track in a playlist."""
        return self._playlist_database.get_track_pos(playlist_id, track_id)

    def get_min_pos(self, playlist_id):
        """Return the minimum position of a track in the database."""
        return self._playlist_database.get_min_pos(playlist_id)

    def get_max_pos(self, playlist_id):
        """Return the largest position of a track in the playlist."""
        return self._playlist_database.get_max_pos(playlist_id)

    def verify_albums(self):
        """Verify and remove trackless albums from database."""
        albums = self.get_all_albums()
        for album_id in albums:
            album_tracklist = self.get_album_tracklist(album_id)
            if not album_tracklist:
                self.delete_album(album_id)

    def verify_artists(self):
        """Verify and remove trackless artists from database."""
        artists = self.get_all_artists()
        for artist_id in artists:
            artist_tracklist = self.get_artist_tracklist(artist_id)
            if not artist_tracklist:
                self.delete_artist(artist_id)

    def delete_album(self, album_id):
        """Delete an album from the database."""
        return self._albums_database.delete_album(album_id)

    def delete_artist(self, artist_id):
        """Delete an album from the database."""
        return self._artist_database.delete_artist(artist_id)
