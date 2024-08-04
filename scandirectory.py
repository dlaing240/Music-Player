from pathlib import Path
from musicdatabase import MusicDatabase
import mutagen  # to get audio file meta-data
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3


class DirectoryScan:
    def __init__(self, music_database: MusicDatabase, directories):
        self.music_database = music_database
        self.directories = directories
        self.new_tracks_stack = []

    def scan_directory(self):
        """
        Scans directories for mp3 files
        """
        no_new_tracks = True
        for directory in self.directories:
            music_files = Path(directory).glob("*.mp3")

            for file_path in music_files:
                file_path_str = str(file_path)
                print(file_path_str)

                # Need to check whether file path is already in the database
                if self.music_database.track_exists(file_path_str):
                    print(f"Track with path: {file_path_str} was found in database")
                else:
                    no_new_tracks = False
                    print(f"Track with path: {file_path_str} was not found in database")

                    # Obtain track metadata using mutagen
                    audio = MP3(file_path, ID3=EasyID3)
                    track_name = str(audio.get('title', ['Unknown Title'])[0])
                    artist = str(audio.get('artist', ['Unknown Artist'])[0])
                    album = str(audio.get('album', ['Unknown Album'])[0])
                    track_number = int(audio.get('tracknumber', [-1])[0])
                    release_date = str(audio.get('date', ['Unknown Date'])[0])
                    duration = audio.info.length
                    genre = str(audio.get('genre', ['Unknown Genre']))
                    album_artist = str(audio.get('albumartist', ['Unknown Album Artist'])[0])

                    self._check_to_add_artist(artist)
                    self._check_to_add_album(album, artist, release_date)
                    self._check_to_add_track(track_name, artist, album, track_number, release_date, genre, duration, file_path_str)

        if no_new_tracks:
            print("No new tracks found")

    def _check_to_add_artist(self, artist_name):
        if self.music_database.artist_exists(artist_name):
            return

        self.music_database.insert_artist(artist_name)
        return

    def _check_to_add_album(self, album_name, artist, release_date):
        if self.music_database.album_exists(album_name, artist, release_date):
            return

        self.music_database.insert_album(album_name, artist, release_date)
        return

    def _check_to_add_track(self, track_name, artist, album, track_number, release_date, genre, duration, file_path_str):
        if self.music_database.track_is_duplicate(track_name, artist, album,
                                                  release_date) and track_name != "Unknown Title":
            print("Track is duplicate. Not added to Database.")
            return

        print("Attempting to add track to database")
        self.music_database.insert_track(track_name, artist, album, track_number, release_date, genre, duration, file_path_str)

        # Check the file path can now be found in the database
        if self.music_database.track_exists(file_path_str):
            print("Track added successfully")
        return

