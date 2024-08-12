from musicdatabase import MusicDatabase
from scandirectory import DirectoryScan
from mixercontroller import MixerController
from root import Root
from sidebarframe import SideBarFrame
from headerframe import HeaderFrame
from tracklistframe import TrackListFrame
from playbarframe import PlayBarFrame
from tracklist import TrackList
from logo import Logo


class App:
    """A music player app."""

    def __init__(self):
        """Initialise the components of the application."""
        database_path = "tracks.db"
        directories_file = "directories.txt"
        self.music_database = MusicDatabase(database_path)

        self.directory_scan = DirectoryScan(self.music_database, directories_file)
        self.track_list = TrackList(self.music_database)

        self.root = Root()

        # Initialise Controllers
        self.mixer_controller = MixerController(
            self.music_database,
            self.track_list,
            self.root
        )
        # Initialise UI Frames
        self.side_bar_frame = SideBarFrame(self.root, self.track_list)
        self.header_frame = HeaderFrame(
            self.root,
            self.track_list,
            self.mixer_controller,
            self.music_database,
            self.side_bar_frame,
            self.directory_scan
        )
        self.play_bar_frame = PlayBarFrame(
            self.root,
            self.mixer_controller,
            self.music_database
        )
        self.track_list_frame = TrackListFrame(
            self.root,
            self.music_database,
            self.mixer_controller,
            self.play_bar_frame,
            self.track_list,
            self.side_bar_frame,
            self.directory_scan,
            self.header_frame
        )
        self.logo = Logo(self.root)
        self.logo.grid(row=0, column=0, padx=2, pady=2, sticky="news")

    def startup(self):
        """Call startup methods."""
        self.directory_scan.scan_directory()  # Check for new music files
        self.track_list.get_collection()  # Start up showing all tracks

    def run(self):
        """Begin running the app."""
        self.startup()
        self.root.mainloop()


my_app = App()
if __name__ == "__main__":
    my_app.run()

