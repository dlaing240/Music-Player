import sqlite3

from artistsdatabase import ArtistsDatabase


class AlbumsDatabase:
    """
    Class responsible for handling operations with the albums database
    """

    def __init__(self, db_path, artist_database: ArtistsDatabase):
        self.db_path = db_path
        self.artist_database = artist_database

        self.create_database()

    def create_database(self):
        """
        Creates the albums table if it doesn't already exist
        :return:
        """
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        # Albums database
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
        Checks whether the given album can be found in the database
        """
        artist_id = self.artist_database.get_artist_id(artist)

        con = sqlite3.connect(self.db_path)
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
        Adds the given album details to the database
        """
        artist_id = self.artist_database.get_artist_id(artist)

        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        cur.execute('''
        INSERT INTO albums (album_name, release_date, artist_id)
        VALUES (?, ?, ?)
        ''', (album_name, release_date, artist_id))
        con.commit()
        con.close()

    def get_album_id(self, album_name, release_date):
        """
        Returns an album's album_id
        """
        con = sqlite3.connect(self.db_path)
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
        con = sqlite3.connect(self.db_path)
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
        Method used to get the album data corresponding to the
        provided album_ids
        """
        id_tuple = tuple(album_ids)
        expression = '(' + ','.join('?' for _ in id_tuple) + ')'

        con = sqlite3.connect(self.db_path)
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
            artist_name = self.artist_database.get_artist_name(artist_id)
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
        """
        Method to get a list of all album_ids in the albums database
        """
        con = sqlite3.connect(self.db_path)
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
        """
        Method to get the ordered tracklist for an album.
        """
        con = sqlite3.connect(self.db_path)
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
