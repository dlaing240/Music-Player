from pathlib import Path
from musicdatabase import MusicDatabase
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3


class DirectoryScan:
    """
    Class to scan directories for music files to add to the database.

    Attributes
    ----------
    directories_updated_observers : list

    Methods
    -------
    get_directories():
        Return a list of the directories in the directories text file
    add_directory(directory_path):
        Add a directory to the file of directories.
    remove_directory(directory_path):
        Remove a directory from the directories file.
    scan_directory():
        Scan directories for music files.
    """
    def __init__(self, music_database: MusicDatabase, directories_file):
        """
        Initialise a `DirectoryScan` instance.

        Parameters
        ----------
        music_database : MusicDatabase
            Instance of `MusicDatabase`
        directories_file : str
            Path to a text file containing the directories to scan.
        """
        self._music_database = music_database
        self._directories_file = directories_file
        self._unverified_paths = set()
        self.directories_updated_observers = []

    def _update_directories(self, directories):
        """Rewrite the directories to the directories file."""
        with open(self._directories_file, 'w') as f:
            for directory in directories:
                f.write(directory+'\n')

    def mp3_found(self, file_path):
        """Process a discovered mp3 file."""
        file_path_str = str(file_path)

        # Need to check whether file path is already in the database
        if self._music_database.track_exists(file_path_str):
            # File found in database - filepath is verified
            self._unverified_paths.remove(file_path_str)
        else:
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
        """Check if a new artist should be added to the database."""
        if self._music_database.artist_exists(artist_name):
            return

        self._music_database.insert_artist(artist_name)
        return

    def _check_to_add_album(self, album_name, artist, release_date):
        """Check if a new album should be added to the database."""
        if self._music_database.album_exists(album_name, artist, release_date):
            return

        self._music_database.insert_album(album_name, artist, release_date)
        return

    def _check_to_add_track(self, track_name, artist, album,
                            track_number, release_date, genre,
                            duration, file_path_str):
        """Check if a new track should be added to the database."""
        # Check whether it's a duplicate
        if (self._music_database.track_is_duplicate(track_name, artist,
                                                    album, release_date)
                and track_name != "Unknown Title"):
            return

        self._music_database.insert_track(track_name, artist, album,
                                          track_number, release_date,
                                          genre, duration, file_path_str)

    def get_directories(self):
        """Return a list of the directories in the directories text file."""
        try:
            with open(self._directories_file, 'r') as f:
                raw_directories = f.readlines()
                # clean whitespace and remove any empty strings
                directories = [directory.strip() for directory in raw_directories if directory.strip()]
        except FileNotFoundError:
            with open(self._directories_file, 'w') as f:
                return []

        directories_updated = False
        for directory in directories:
            path = Path(directory)
            if not path.exists() and not path.is_dir():
                print(directory, " is an invalid directory")
                directories.remove(directory)
                directories_updated = True

        if directories_updated:
            self._update_directories(directories)

        return directories

    def add_directory(self, directory_path):
        """Add a directory to the file of directories."""
        with open(self._directories_file, 'a') as f:
            f.write(directory_path + '\n')

        self.scan_directory()

        for observer in self.directories_updated_observers:
            observer.received_directories_updated_signal()

    def remove_directory(self, directory_path):
        """Remove a directory from the directories file."""
        directories = self.get_directories()
        directories.remove(directory_path)
        self._update_directories(directories)

    def scan_directory(self):
        """
        Scan directories for music files.

        Currently scans for mp3 files only.
        """
        # While scanning, use the results to verify tracks in the database
        self._unverified_paths = set(self._music_database.get_all_paths())

        for directory in self.get_directories():
            mp3_files = Path(directory).glob("*.mp3")

            for file_path in mp3_files:
                self.mp3_found(file_path)

        # if any database tracks are unverified after the scan
        if self._unverified_paths:
            self._music_database.remove_by_paths(self._unverified_paths)

        # Verify the albums and artists in the database
        self._music_database.verify_albums()
        self._music_database.verify_artists()

    def verify_paths(self, path_list):
        """
        Verify a list of file paths and remove invalid tracks.

        Unused.
        """
        invalid_paths = []

        for path_str in path_list:
            path = Path(path_str)
            if not path.exists() or not path.is_file():
                invalid_paths.append(path_str)

        self._music_database.remove_by_paths(invalid_paths)

    def verify_all_paths(self):
        """
        Verify all paths in the database.

        Unused.
        """
        file_paths = self._music_database.get_all_paths()
        self.verify_paths(file_paths)
