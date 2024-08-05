import sqlite3


class ArtistsDatabase:
    """
    Class responsible for handling operations with the artists database
    """
    def __init__(self, db_path):
        self.db_path = db_path
        self.create_database()

    def create_database(self):
        """
        Creates the artists table if it doesn't already exist
        """
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        # Artist database
        cur.execute('''CREATE TABLE IF NOT EXISTS artists(
                    artist_id INTEGER PRIMARY KEY,
                    artist_name TEXT NOT NULL)''')
        con.commit()
        con.close()

    def artist_exists(self, artist_name):
        """
        Checks whether the provided artist is in the database
        """
        if self.get_artist_id(artist_name):
            return True
        return False

    def insert_artist(self, artist_name):
        """
        Adds the artist to the database
        """
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        cur.execute('''INSERT INTO artists (artist_name)
                    VALUES (?)''',
                    (artist_name,))
        con.commit()
        con.close()

    def get_artist_id(self, artist_name):
        """
        Returns the artist's artist_id
        """
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        cur.execute('''SELECT artist_id
                    FROM artists
                    WHERE artist_name = ?''',
                    (artist_name,))
        artist = cur.fetchone()
        con.close()

        if artist:
            artist_id = artist[0]
        else:
            artist_id = None

        return artist_id

    def get_artist_name(self, artist_id):
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        cur.execute('''SELECT artist_name
                    FROM artists
                    WHERE artist_id = ?''',
                    (artist_id,))
        artist = cur.fetchone()
        con.close()
        artist_name = artist[0]
        return artist_name

    def get_all_artists(self):
        """
        Gets a list of all the artist_ids in the database
        """
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        cur.execute('''SELECT artist_id, artist_name
                    FROM artists
                    ORDER BY artist_name 
                    COLLATE NOCASE''')
        artist_rows = cur.fetchall()
        con.close()

        artists = []
        for artist in artist_rows:
            artists.append(artist[0])
        return artists

    def get_artist_metadata(self, artist_ids):
        """
        Gets the database data corresponding to each artist in the given list
        of artist_ids
        """
        id_tuple = tuple(artist_ids)
        expression = '(' + ','.join('?' for _ in id_tuple) + ')'

        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        cur.execute(f'''SELECT artist_id, artist_name
                    FROM artists
                    WHERE artist_id IN {expression}
                    ''', id_tuple)
        artist_rows = cur.fetchall()

        artists_info = {}
        for row in artist_rows:
            artist_id = row[0]
            artist_name = row[1]
            artist = {
                "album_id": artist_id,
                "artist_name": artist_name
            }
            artists_info[artist_id] = artist

        return artists_info

    def get_artist_tracklist(self, artist_id):
        """
        Gets the list of tracks by the provided artist
        """
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        cur.execute('''SELECT track_id 
                    FROM tracks 
                    WHERE artist_id = ?''',
                    (artist_id,))
        tracks_rows = cur.fetchall()
        con.close()

        tracks = []
        for track_data in tracks_rows:
            tracks.append(track_data[0])
        return tracks

    def get_artist_albumlist(self, artist_id):
        """
        Gets a list of albums by the artist
        """
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        cur.execute('''SELECT album_id, album_name 
                    FROM albums 
                    WHERE artist_id = ?''',
                    (artist_id,))
        tracks_rows = cur.fetchall()
        con.close()

        albums = {}
        for album_data in tracks_rows:
            albums[album_data[0]] = album_data[1]
        print(albums)
        return albums
