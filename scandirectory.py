from pathlib import Path
from musicdatabase import MusicDatabase
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3

from paths import paths


class DirectoryScan:
    def __init__(self, music_database: MusicDatabase, directories_file):
        self.music_database = music_database
        self.directories_file = directories_file
        self.directories = paths
        self.new_tracks_stack = []
        self.unverified_paths = set()

        self.directories_updated_observers = []

    def get_directories(self):
        try:
            with open(self.directories_file, 'r') as f:
                raw_directories = f.readlines()
                # clean whitespace and remove any empty strings
                directories = [directory.strip() for directory in raw_directories if directory.strip()]
        except FileNotFoundError:
            with open(self.directories_file, 'w') as f:
                return []

        directories_updated = False
        for directory in directories:
            path = Path(directory)
            if not path.exists() and not path.is_dir():
                print(directory, " is an invalid directory")
                directories.remove(directory)
                directories_updated = True

        if directories_updated:
            self.update_directories(directories)

        return directories

    def update_directories(self, directories):
        """
        Rewrites the directories to the directories file

        Parameters
        ----------
        directories

        Returns
        -------

        """
        with open(self.directories_file, 'w') as f:
            for directory in directories:
                f.write(directory+'\n')

    def add_directory(self, directory_path):
        """
        Adds a directory to the file of directories

        Parameters
        ----------
        directory_path

        Returns
        -------

        """
        with open(self.directories_file, 'a') as f:
            f.write(directory_path + '\n')

        self.scan_directory()

        for observer in self.directories_updated_observers:
            observer.received_directories_updated_signal()

    def remove_directory(self, directory_path):
        """
        Removes the directory from the directories file

        Parameters
        ----------
        directory_path

        Returns
        -------

        """
        directories = self.get_directories()
        directories.remove(directory_path)
        self.update_directories(directories)

    def scan_directory(self):
        """
        Scans directories for mp3 files
        """
        # While scanning, use the results to verify tracks in the database
        self.unverified_paths = set(self.music_database.get_all_paths())

        for directory in self.get_directories():
            mp3_files = Path(directory).glob("*.mp3")

            for file_path in mp3_files:
                self.mp3_found(file_path)

        # if any database tracks are unverified after the scan
        if self.unverified_paths:
            self.music_database.remove_by_paths(self.unverified_paths)

    def verify_paths(self, path_list):
        """
        Verifies a list of file paths

        Parameters
        ----------
        path_list

        Returns
        -------

        """
        invalid_paths = []

        for path_str in path_list:
            path = Path(path_str)
            if not path.exists() or not path.is_file():
                invalid_paths.append(path_str)

        self.music_database.remove_by_paths(invalid_paths)

    def verify_all_paths(self):
        """
        Verifies all paths in the database

        Returns
        -------

        """
        file_paths = self.music_database.get_all_paths()
        self.verify_paths(file_paths)

    def mp3_found(self, file_path):
        file_path_str = str(file_path)

        # Need to check whether file path is already in the database
        if self.music_database.track_exists(file_path_str):
            # File found in database - filepath is verified
            self.unverified_paths.remove(file_path_str)
        else:
            no_new_tracks = False
            # Obtain track metadata using mutagen
            audio = MP3(file_path, ID3=EasyID3)
            track_name = str(audio.get('title', ['Unknown Title'])[0])
            artist = str(audio.get('artist', ['Unknown Artist'])[0])
            album = str(audio.get('album', ['Unknown Album'])[0])
            track_number = int(audio.get('tracknumber', [-1])[0])
            release_date = str(audio.get('date', ['Unknown Date'])[0])
            duration = audio.info.length
            genre = str(audio.get('genre', ['Unknown Genre']))
            album_artist = str(
                audio.get('albumartist', ['Unknown Album Artist'])[0]
            )

            self._check_to_add_artist(artist)
            self._check_to_add_album(album, artist, release_date)
            self._check_to_add_track(track_name, artist, album,
                                     track_number, release_date,
                                     genre, duration, file_path_str)

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

    def _check_to_add_track(self, track_name, artist, album,
                            track_number, release_date, genre,
                            duration, file_path_str):
        # Check whether it's a duplicate
        if (self.music_database.track_is_duplicate(track_name, artist,
                                                   album, release_date)
                and track_name != "Unknown Title"):
            return

        self.music_database.insert_track(track_name, artist, album,
                                         track_number, release_date,
                                         genre, duration, file_path_str)
