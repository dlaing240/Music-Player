from artistsdatabase import ArtistsDatabase
from albumsdatabase import AlbumsDatabase
from trackdatabase import TrackDatabase
from playlistsdatabase import PlaylistDatabase


class MusicDatabase:
    """
    Class which acts as an interface for the database operations classes
    """
    def __init__(self, db_path):
        self.artist_database = ArtistsDatabase(db_path)
        self.albums_database = AlbumsDatabase(db_path, self.artist_database)
        self.playlist_database = PlaylistDatabase(db_path)
        self.tracks_database = TrackDatabase(db_path,
                                             self.artist_database,
                                             self.albums_database,
                                             self.playlist_database)

    def create_database(self):
        """
        Creates the database tables if they don't already exist
        """
        self.artist_database.create_database()
        self.albums_database.create_database()
        self.tracks_database.create_database()
        self.playlist_database.create_tables()

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
        return self.albums_database.album_exists(album_name,
                                                 artist,
                                                 release_date)

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

    def get_album_title(self, album_id):
        return self.albums_database.get_album_title(album_id)

    def get_album_metadata(self, album_ids):
        """
        Method used to get the album data corresponding to the provided
        album_ids
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
        Checks whether the track data matches a track that's already in the
        database
        """
        return self.tracks_database.track_is_duplicate(track_name, artist,
                                                       album, release_date)

    def insert_track(self, track_name, artist, album, track_number,
                     release_date, genre, duration, file_path):
        """
        Adds the track to the database
        """
        self.tracks_database.insert_track(track_name, artist, album,
                                          track_number, release_date,
                                          genre, duration, file_path)

    def get_all_tracks(self):
        """
        Returns a list of all track_ids in the database
        """
        return self.tracks_database.get_all_tracks()

    def get_track_metadata(self, id_list):
        """
        Gets the database data corresponding to the tracks in the
        list of track_ids.
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
        Gets the database data corresponding to each artist in the
        given list of artist_ids
        """
        return self.artist_database.get_artist_metadata(artist_ids)

    def get_artist_albumlist(self, artist_id):
        """
        Gets a list of albums by the artist
        """
        return self.artist_database.get_artist_albumlist(artist_id)

    def create_playlist(self, playlist_name):
        return self.playlist_database.create_playlist(playlist_name)

    def add_to_playlist(self, track_id, playlist_id):
        return self.playlist_database.add_to_playlist(track_id, playlist_id)

    def remove_from_playlist(self, track_id, playlist_id):
        return self.playlist_database.remove_from_playlist(track_id, playlist_id)

    def get_playlist_tracks(self, playlist_id):
        return self.playlist_database.get_playlist_tracks(playlist_id)

    def get_playlists(self):
        return self.playlist_database.get_playlists()

    def get_playlist_name(self, playlist_id):
        return self.playlist_database.get_playlist_name(playlist_id)

    def get_all_paths(self):
        """
        Returns all the file paths in the database

        Returns
        -------

        """
        return self.tracks_database.get_all_paths()

    def remove_by_paths(self, file_paths):
        """
        Removes the database entry corresponding to the file_path given

        Parameters
        ----------
        file_paths

        Returns
        -------

        """
        return self.tracks_database.remove_by_paths(file_paths)

    def delete_playlist(self, playlist_id):
        """
        Deletes the playlist from the database

        Parameters
        ----------
        playlist_id

        Returns
        -------

        """
        return self.playlist_database.delete_playlist(playlist_id)

    def swap_positions(self, playlist_id, pos_1, pos_2):
        """
        Swaps the positions of two tracks in a playlist

        Parameters
        ----------
        playlist_id
        pos_1
        pos_2

        Returns
        -------

        """
        return self.playlist_database.swap_positions(playlist_id, pos_1, pos_2)

    def get_track_pos(self, playlist_id, track_id):
        return self.playlist_database.get_track_pos(playlist_id, track_id)

    def get_min_pos(self, playlist_id):
        return self.playlist_database.get_min_pos(playlist_id)

    def get_max_pos(self, playlist_id):
        return self.playlist_database.get_max_pos(playlist_id)
