import sqlite3

from artistsdatabase import ArtistsDatabase


class AlbumsDatabase:
    """
    Class for handling database operations related to albums.

    This class is not used directly by other components, as the
    `MusicDatabase` class provides the interface for database operations.
    """

    def __init__(self, db_path, artist_database: ArtistsDatabase):
        """
        Initialise an `AlbumsDatabase` instance.

        Parameters
        ----------
        db_path : str
            The path to the database.
        artist_database : ArtistsDatabase
            The instance of the `ArtistsDatabase` class.
        """
        self._db_path = db_path
        self._artist_database = artist_database

    def create_database(self):
        """Creates the `albums` table if it doesn't already exist"""
        con = sqlite3.connect(self._db_path)
        cur = con.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS albums (
                album_id INTEGER PRIMARY KEY,
                album_name TEXT NOT NULL,
                release_date TEXT NOT NULL,
                artist_id INTEGER NOT NULL,
                FOREIGN KEY(artist_id) REFERENCES artists(artist_id)
            )
        ''')
        con.commit()
        con.close()

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
        artist_id = self._artist_database.get_artist_id(artist)

        con = sqlite3.connect(self._db_path)
        cur = con.cursor()
        cur.execute('''
        SELECT 1 FROM albums 
        WHERE album_name = ?
        AND artist_id = ?
        AND release_date = ?
        ''', (album_name, artist_id, release_date))
        exists = cur.fetchone() is not None
        con.close()
        return exists

    def insert_album(self, album_name, artist, release_date):
        """
        Insert an album into the database.

        Parameters
        ----------
        album_name : str
            The title of the album.
        artist : str
            The name of the artist
        release_date : str
            The release date of the album.
        """
        artist_id = self._artist_database.get_artist_id(artist)

        con = sqlite3.connect(self._db_path)
        cur = con.cursor()
        cur.execute('''
        INSERT INTO albums (album_name, release_date, artist_id)
        VALUES (?, ?, ?)
        ''', (album_name, release_date, artist_id))
        con.commit()
        con.close()

    def get_album_id(self, album_name, release_date):
        """
        Return an album's unique identifier

        Parameters
        ----------
        album_name : str
            The title of the album.
        release_date : str
            The release date of the album.

        Returns
        -------
        int
            The unique identifier for the album.
        """
        con = sqlite3.connect(self._db_path)
        cur = con.cursor()
        # Write query
        cur.execute(
            '''SELECT album_id 
            FROM albums
            WHERE album_name = ?
            AND release_date = ?
            ''',
            (album_name, release_date)
        )
        album = cur.fetchone()
        con.close()

        if album:
            album_id = album[0]
        else:
            album_id = None
        return album_id

    def get_album_title(self, album_id):
        """Return the album's title from its identifier."""
        con = sqlite3.connect(self._db_path)
        cur = con.cursor()
        cur.execute(
            '''SELECT album_name
            FROM albums
            WHERE album_id = ?''',
            (album_id,)
        )
        album = cur.fetchone()
        con.close()
        album_name = album[0]
        return album_name

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
        id_tuple = tuple(album_ids)
        expression = '(' + ','.join('?' for _ in id_tuple) + ')'

        con = sqlite3.connect(self._db_path)
        cur = con.cursor()
        cur.execute(f'''
        SELECT album_id, album_name, release_date, artist_id
        FROM albums
        WHERE album_id IN {expression}
        ''', id_tuple)

        albums_rows = cur.fetchall()

        albums_info = {}
        for row in albums_rows:
            album_id = row[0]
            artist_id = row[3]
            artist_name = self._artist_database.get_artist_name(artist_id)
            album = {
                "album_id": album_id,
                "album_name": row[1],
                "release_date": row[2],
                "artist_id": artist_id,
                "artist_name": artist_name
            }
            albums_info[album_id] = album

        return albums_info

    def get_all_albums(self):
        """Return a list of every `album_id` in the albums database."""
        con = sqlite3.connect(self._db_path)
        cur = con.cursor()
        cur.execute(
            '''SELECT album_id, album_name
            FROM albums
            ORDER BY album_name
            COLLATE NOCASE'''
        )
        album_rows = cur.fetchall()
        con.close()

        albums = []
        for album in album_rows:
            albums.append(album[0])
        return albums

    def get_album_tracklist(self, album_id):
        """Return a list of `track_id`s in the given album."""
        con = sqlite3.connect(self._db_path)
        cur = con.cursor()
        cur.execute(
            '''SELECT track_id
            FROM tracks
            WHERE album_id = ? 
            ORDER BY track_number''',
            (album_id,)
        )
        tracks_rows = cur.fetchall()
        con.close()

        tracks = []
        for track_data in tracks_rows:
            tracks.append(track_data[0])

        return tracks

    def delete_album(self, album_id):
        """Delete an album from the database."""
        con = sqlite3.connect(self._db_path)
        cur = con.cursor()
        cur.execute('''
            DELETE FROM albums WHERE album_id = ?
        ''', (album_id,))
        con.commit()
        con.close()
