import sqlite3

from artistsdatabase import ArtistsDatabase
from albumsdatabase import AlbumsDatabase
from playlistsdatabase import PlaylistDatabase


class TrackDatabase:
    def __init__(self, db_path,
                 artist_database: ArtistsDatabase,
                 albums_database: AlbumsDatabase,
                 playlist_database: PlaylistDatabase):
        self.db_path = db_path
        self.artist_database = artist_database
        self.albums_database = albums_database
        self.playlist_database = playlist_database
        self.create_database()

    def create_database(self):
        """
        Creates the tracks table if it doesn't already exist
        """
        con = sqlite3.connect(self.db_path)
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
        """
        Checks whether the file path corresponds to a track in the database
        """
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        cur.execute('SELECT 1 FROM tracks WHERE file_path = ?', (file_path,))
        exists = cur.fetchone() is not None
        con.close()
        return exists

    def track_is_duplicate(self, track_name, artist, album, release_date):
        """
        Checks whether the track data matches a track that's already in the
        database
        """
        artist_id = self.artist_database.get_artist_id(artist)
        album_id = self.albums_database.get_album_id(album, release_date)

        con = sqlite3.connect(self.db_path)
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
        """
        Adds the track to the database
        """
        artist_id = self.artist_database.get_artist_id(artist)
        album_id = self.albums_database.get_album_id(album, release_date)

        con = sqlite3.connect(self.db_path)
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
        """
        Returns a list of all track_ids in the database
        """
        con = sqlite3.connect(self.db_path)
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
        Gets the database data corresponding to the tracks in the list of
        track_ids.
        """
        id_tuple = tuple(id_list)
        expression = '(' + ','.join('?' for _ in id_tuple) + ')'

        con = sqlite3.connect(self.db_path)
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
        """
        Returns the file path of the given track
        """
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        cur.execute('SELECT file_path FROM tracks WHERE track_id = ?',
                    (track_id,))
        file_path = cur.fetchone()[0]
        con.close()

        return file_path

    def get_duration(self, track_id):
        """
        Returns the duration of the song
        """
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        cur.execute('SELECT duration FROM tracks WHERE track_id = ?',
                    (track_id,))
        duration = cur.fetchone()[0]
        con.close()
        return duration

    def get_all_paths(self):
        """
        Returns all the file paths in the database

        Returns
        -------

        """
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        cur.execute('''
            SELECT file_path FROM tracks
        ''')
        path_rows = cur.fetchall()

        paths = [row[0] for row in path_rows]
        return paths

    def remove_by_paths(self, file_paths):
        """
        Removes the database entry corresponding to the file_path given

        Parameters
        ----------
        file_paths

        Returns
        -------

        """

        con = sqlite3.connect(self.db_path)
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
            self.playlist_database.remove_from_all(track_id)
