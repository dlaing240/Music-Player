import sqlite3

from artistsdatabase import ArtistsDatabase
from albumsdatabase import AlbumsDatabase
from playlistsdatabase import PlaylistDatabase


class TrackDatabase:
    """
    Class for handling database operations related to tracks.

    This class is not used directly by other components, as the
    `MusicDatabase` class provides the interface for database operations.
    """

    def __init__(self, db_path,
                 artist_database: ArtistsDatabase,
                 albums_database: AlbumsDatabase,
                 playlist_database: PlaylistDatabase):
        """
        Initialise a `TrackDatabase` instance.

        Parameters
        ----------
        db_path : str
            Path to the database.
        artist_database : ArtistsDatabase
            Instance of `ArtistsDatabase.
        albums_database : AlbumsDatabase
            Instance of `AlbumsDatabase`.
        playlist_database : PlaylistDatabase
            Instance of `PlaylistDatabase`.
        """
        self._db_path = db_path
        self._artist_database = artist_database
        self._albums_database = albums_database
        self._playlist_database = playlist_database
        self.create_database()

    def create_database(self):
        """Create the tracks table if it doesn't exist."""
        con = sqlite3.connect(self._db_path)
        cur = con.cursor()

        # Tracks database
        cur.execute('''
            CREATE TABLE IF NOT EXISTS tracks (
                track_id INTEGER PRIMARY KEY,
                track_name TEXT NOT NULL,
                release_date TEXT NOT NULL,
                genre TEXT NOT NULL,
                duration REAL NOT NULL,
                file_path  TEXT NOT NULL UNIQUE,
                track_number INTEGER NOT NULL,
                album_id INTEGER NOT NULL,
                artist_id INTEGER NOT NULL,
                FOREIGN KEY(album_id) REFERENCES albums(album_id),
                FOREIGN KEY (artist_id) REFERENCES artists(artist_id)
            ) 
        ''')
        con.commit()
        con.close()

    def track_exists(self, file_path):
        """Return True if the file path is in the database and False otherwise."""
        con = sqlite3.connect(self._db_path)
        cur = con.cursor()
        cur.execute('SELECT 1 FROM tracks WHERE file_path = ?', (file_path,))
        exists = cur.fetchone() is not None
        con.close()
        return exists

    def track_is_duplicate(self, track_name, artist, album, release_date):
        """Return True if track is already in the database, False otherwise."""
        artist_id = self._artist_database.get_artist_id(artist)
        album_id = self._albums_database.get_album_id(album, release_date)

        con = sqlite3.connect(self._db_path)
        cur = con.cursor()
        cur.execute('''
            SELECT 1 FROM tracks
            WHERE track_name = ?
            AND artist_id = ?
            AND album_id = ?
            AND release_date = ?
        ''', (track_name, artist_id, album_id, release_date))

        is_duplicate = cur.fetchone() is not None
        con.close()
        return is_duplicate

    def insert_track(self, track_name, artist, album, track_number,
                     release_date, genre, duration, file_path):
        """Add a track to the database."""
        artist_id = self._artist_database.get_artist_id(artist)
        album_id = self._albums_database.get_album_id(album, release_date)

        con = sqlite3.connect(self._db_path)
        cur = con.cursor()
        cur.execute('''
            INSERT INTO tracks (
                track_name,
                artist_id, 
                album_id, 
                track_number, 
                release_date, 
                genre, 
                duration, 
                file_path
                )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (track_name, artist_id, album_id, track_number,
              release_date, genre, duration, file_path))
        con.commit()
        con.close()

    def get_all_tracks(self):
        """Return a list of all `track_id`s in the database."""
        con = sqlite3.connect(self._db_path)
        cur = con.cursor()
        cur.execute('''
            SELECT track_id 
            FROM tracks 
            ORDER BY track_name 
            COLLATE NOCASE
            ''')
        tracks_rows = cur.fetchall()
        con.close()

        tracks = []
        for track_data in tracks_rows:
            tracks.append(track_data[0])

        return tracks

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
        id_tuple = tuple(id_list)
        expression = '(' + ','.join('?' for _ in id_tuple) + ')'

        con = sqlite3.connect(self._db_path)
        cur = con.cursor()
        cur.execute(f'''
            SELECT track_id,
                track_name,
                artist_id, 
                album_id, 
                release_date, 
                file_path, 
                duration
            FROM tracks
            WHERE track_id IN {expression}''', id_tuple)
        tracks_rows = cur.fetchall()
        con.close()

        tracks = {}
        for track_data in tracks_rows:
            track_id = track_data[0]
            track = {
                "track_id": track_id,
                'track_name': track_data[1],
                'artist': track_data[2],
                'album': track_data[3],
                'release_date': track_data[4],
                'file_path': track_data[5],
                'duration': track_data[6]
            }
            tracks[track_id] = track

        return tracks

    def get_path(self, track_id):
        """Return the file path of the given track."""
        con = sqlite3.connect(self._db_path)
        cur = con.cursor()
        cur.execute('SELECT file_path FROM tracks WHERE track_id = ?',
                    (track_id,))
        file_path = cur.fetchone()[0]
        con.close()

        return file_path

    def get_duration(self, track_id):
        """Return the duration of a track."""
        con = sqlite3.connect(self._db_path)
        cur = con.cursor()
        cur.execute('SELECT duration FROM tracks WHERE track_id = ?',
                    (track_id,))
        duration = cur.fetchone()[0]
        con.close()
        return duration

    def get_all_paths(self):
        """Return a list containing all the file paths in the database."""
        con = sqlite3.connect(self._db_path)
        cur = con.cursor()
        cur.execute('''
            SELECT file_path FROM tracks
        ''')
        path_rows = cur.fetchall()

        paths = [row[0] for row in path_rows]
        return paths

    def remove_by_paths(self, file_paths):
        """Remove database entries corresponding to the file paths."""
        con = sqlite3.connect(self._db_path)
        cur = con.cursor()

        track_ids = []

        for file_path in file_paths:
            cur.execute('''
            SELECT track_id
            FROM tracks
            WHERE file_path = ?
            ''', (file_path,))
            track_id = cur.fetchone()[0]
            track_ids.append(track_id)

            cur.execute('''
            DELETE FROM tracks WHERE file_path = ?
            ''', (file_path,))

        con.commit()
        con.close()
        for track_id in track_ids:
            self._playlist_database.remove_from_all(track_id)
