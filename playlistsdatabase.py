import sqlite3


class PlaylistDatabase:
    """
    Class for handling database operations involving playlists.

    This class is not used directly by other components, as the
    `MusicDatabase` class provides the interface for database operations.
    """

    def __init__(self, db_path):
        """Initialise a `PlaylistDatabase` instance."""
        self._db_path = db_path
        self.create_tables()

    def create_tables(self):
        """Create the `playlists` and `playlist_tracks` tables if they don't exist."""
        con = sqlite3.connect(self._db_path)
        cur = con.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS playlists (
                playlist_id INTEGER PRIMARY KEY,
                playlist_name TEXT NOT NULL
            )
        ''')

        cur.execute('''
            CREATE TABLE IF NOT EXISTS playlist_tracks (
                identifier INTEGER PRIMARY KEY,
                playlist_id INTEGER NOT NULL,
                track_id INTEGER NOT NULL,
                position INTEGER NOT NULL,
                FOREIGN KEY (playlist_id) REFERENCES playlists(playlist_id),
                FOREIGN KEY (track_id) REFERENCES tracks(track_id)
                UNIQUE (playlist_id, track_id, position)
            )
        ''')

        con.commit()
        con.close()

    def create_playlist(self, playlist_name):
        """Create a new playlist with the given name."""
        con = sqlite3.connect(self._db_path)
        cur = con.cursor()
        cur.execute('''
            INSERT INTO playlists (playlist_name)
            VALUES (?)    
        ''', (playlist_name,))
        con.commit()
        con.close()

    def get_max_pos(self, playlist_id):
        """Return the largest position of a track in the playlist."""
        con = sqlite3.connect(self._db_path)
        cur = con.cursor()

        # Find position of the new track
        cur.execute('''
            SELECT MAX(position) FROM playlist_tracks
            WHERE playlist_id = ?
        ''', (playlist_id,))
        max_position = cur.fetchone()[0]
        if max_position is None:
            max_position = 0

        con.close()
        return max_position

    def get_min_pos(self, playlist_id):
        """Return the minimum position of a track in the database."""
        con = sqlite3.connect(self._db_path)
        cur = con.cursor()

        # Find position of the new track
        cur.execute('''
            SELECT MIN(position) FROM playlist_tracks
            WHERE playlist_id = ?
        ''', (playlist_id,))
        min_position = cur.fetchone()[0]
        if min_position is None:
            min_position = 0

        con.close()
        return min_position

    def add_to_playlist(self, track_id, playlist_id):
        """Add a track to a playlist."""
        con = sqlite3.connect(self._db_path)
        cur = con.cursor()

        max_position = self.get_max_pos(playlist_id)

        cur.execute('''
            INSERT INTO playlist_tracks (playlist_id, track_id, position)
            VALUES (?, ?, ?)    
        ''', (playlist_id, track_id, max_position+1))
        con.commit()
        con.close()

    def remove_from_playlist(self, track_id, playlist_id):
        """Remove a track from a playlist."""
        con = sqlite3.connect(self._db_path)
        cur = con.cursor()
        cur.execute('''
            DELETE FROM playlist_tracks
            WHERE playlist_id = ? AND track_id = ?
        ''', (playlist_id, track_id))
        con.commit()
        con.close()

    def get_playlist_tracks(self, playlist_id):
        """Return the list of tracks in a playlist."""
        con = sqlite3.connect(self._db_path)
        cur = con.cursor()
        cur.execute('''
            SELECT track_id FROM playlist_tracks
            WHERE playlist_id = ?
            ORDER BY position
        ''', (playlist_id,))
        track_rows = cur.fetchall()
        con.close()

        tracks = []
        for row in track_rows:
            tracks.append(row[0])

        return tracks

    def get_playlists(self):
        """Return a list of all playlists in the database."""
        con = sqlite3.connect(self._db_path)
        cur = con.cursor()
        cur.execute('''
            SELECT playlist_id, playlist_name
            FROM playlists       
        ''')
        playlist_rows = cur.fetchall()
        con.close()

        playlists = {}
        for row in playlist_rows:
            playlist_id = row[0]
            playlist_name = row[1]
            playlists[playlist_id] = playlist_name

        return playlists

    def get_playlist_name(self, playlist_id):
        """Return the name of a playlist from its ID."""
        con = sqlite3.connect(self._db_path)
        cur = con.cursor()
        cur.execute('''SELECT playlist_name
                    FROM playlists
                    WHERE playlist_id = ?''',
                    (playlist_id,))
        playlist = cur.fetchone()
        con.close()
        playlist_name = playlist[0]
        return playlist_name

    def remove_from_all(self, track_id):
        """Remove a track from all playlists."""
        con = sqlite3.connect(self._db_path)
        cur = con.cursor()
        cur.execute('''
            SELECT playlist_id
            FROM playlist_tracks
            WHERE track_id = ?
            ''', (track_id,))
        rows = cur.fetchall()
        for row in rows:
            playlist_id = row[0]
            self.remove_from_playlist(track_id, playlist_id)

    def delete_playlist(self, playlist_id):
        """Delete a playlist from the database."""
        con = sqlite3.connect(self._db_path)
        cur = con.cursor()

        # Delete playlist
        cur.execute('''
            DELETE FROM playlists
            WHERE playlist_id = ?
        ''', (playlist_id,))

        # Delete playlist-track pairs for that playlist
        cur.execute('''
            DELETE FROM playlist_tracks
            WHERE playlist_id = ?
        ''', (playlist_id,))

        con.commit()
        con.close()

    def swap_positions(self, playlist_id, pos_1, pos_2):
        """Swap the positions of two tracks in a playlist."""
        con = sqlite3.connect(self._db_path)
        cur = con.cursor()
        # Move track in pos_1 to a temporary position
        cur.execute('''
            UPDATE playlist_tracks
            SET position = -1
            WHERE playlist_id = ? AND position = ?
            ''', (playlist_id, pos_1))

        # Move track in pos_2 to pos_1
        cur.execute('''
                    UPDATE playlist_tracks
                    SET position = ?
                    WHERE playlist_id = ? AND position = ?
                    ''', (pos_1, playlist_id, pos_2))

        # move first track into pos_2
        cur.execute('''
                    UPDATE playlist_tracks
                    SET position = ?
                    WHERE playlist_id = ? AND position = -1
                    ''', (pos_2, playlist_id))

        con.commit()
        con.close()

    def get_track_pos(self, playlist_id, track_id):
        """Return the position of a track in a playlist."""
        con = sqlite3.connect(self._db_path)
        cur = con.cursor()
        cur.execute('''SELECT position
                    FROM playlist_tracks
                    WHERE playlist_id = ? AND track_id = ?  
                    ''', (playlist_id, track_id))
        position = cur.fetchone()[0]
        con.close()
        return position
