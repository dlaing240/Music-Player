import tkinter as tk

from root import Root, colour_scheme

from collectionsheader import CollectionsHeader
from tracklist import TrackList
from mixercontroller import MixerController
from musicdatabase import MusicDatabase
from listheader import ListHeader
from sidebarframe import SideBarFrame
from playlistheader import PlaylistsHeader
from directoriesheader import DirectoriesHeader, DirectoryScan


class HeaderFrame(tk.Frame):
    """
    Frame to contain and display headers.

    Attributes
    ----------
    update_playlist_display_observers : list
        List of observers with the method
        `received_update_playlist_display_signal`

    Methods
    -------
    received_tracklist_updated_signal():
        Display the header for the updated track list.
    received_open_album_list_signal():
        Display the header for the opened album.
    received_open_artist_list_signal():
        Display the header for the opened artist page.
    received_open_queue_signal():
        Display the header for the queue.
    received_open_playlists_signal():
        Display the header for the opened playlist.
    received_open_directories_signal():
        Display the directory list header.
    """

    def __init__(self, parent: Root,
                 tracklist: TrackList,
                 mixer_controller: MixerController,
                 music_database: MusicDatabase,
                 sidebarframe: SideBarFrame,
                 directory_scan: DirectoryScan):
        """
        Initialise a `HeaderFrame` instance.

        Parameters
        ----------
        parent : tk.Widget
            The parent widget of this frame.
        tracklist : TrackList
            Instance of `Tracklist`.
        mixer_controller : MixerController
            Instance of `MixerController`.
        music_database : MusicDatabase
            Instance of `MusicDatabase`.
        sidebarframe : SideBarFrame
            Instance of `SideBarFrame`.
        directory_scan : DirectoryScan
            Instance of `DirectoryScan`.
        """
        super().__init__(parent)
        self._parent = parent
        self._tracklist = tracklist
        self._mixer_controller = mixer_controller
        self._music_database = music_database
        self._sidebarframe = sidebarframe
        self._directory_scan = directory_scan
        self._colour_scheme = colour_scheme

        # listen for updates to the display
        self._tracklist.tracklist_updated_observers.append(self)
        self._sidebarframe.open_artist_list_observers.append(self)
        self._sidebarframe.open_album_list_observers.append(self)
        self._sidebarframe.open_queue_observers.append(self)
        self._sidebarframe.open_playlist_observers.append(self)
        self._sidebarframe.open_directories_observers.append(self)

        self.update_playlist_display_observers = []

        self.padding_size = self._parent.padding_size
        self.grid(row=0, column=1, sticky="news",
                  padx=self.padding_size, pady=self.padding_size)
        self.config(width=640 - self.padding_size*2,
                    height=100 - self.padding_size*2, bg=self._colour_scheme["grey"])
        self._grid_config()

        self._current_header = None
        self._display_collection_header()

    def _grid_config(self):
        """Configure the expansion of the grid."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def _display_collection_header(self):
        """Display the header for the current collection."""
        collection_type = self._tracklist.collection_type
        collection_id = self._tracklist.collection_id
        collection_title = self._tracklist.collection_title
        track_count = len(self._tracklist.get_tracklist())
        duration = self._tracklist.get_total_tracklist_duration()
        if collection_type == "album":
            artist_id = self._music_database.get_album_metadata(
                [collection_id]
            )[collection_id]["artist_id"]
            subtitle = self._music_database.get_artist_name(artist_id)
        else:
            subtitle = None

        collections_header = CollectionsHeader(
            parent=self,
            play_all_command=self._mixer_controller.play_all,
            collection_type=collection_type,
            collection_title=collection_title,
            collection_id=collection_id,
            track_count=track_count,
            duration=duration,
            subtitle=subtitle
        )

        collections_header.grid(row=0, column=0, sticky="news")
        self._current_header = collections_header

    def received_tracklist_updated_signal(self):
        """Display the header for the updated track list."""
        self._current_header.destroy()
        self._display_collection_header()

    def received_open_album_list_signal(self):
        """Display the header for the opened album."""
        self._current_header.destroy()
        album_list_header = ListHeader(self, "Albums")
        album_list_header.grid(row=0, column=0,  sticky="news")
        self._current_header = album_list_header

    def received_open_artist_list_signal(self):
        """Display the header for the opened artist page."""
        self._current_header.destroy()
        artist_list_header = ListHeader(self, "Artists")
        artist_list_header.grid(row=0, column=0, sticky="news")
        self._current_header = artist_list_header

    def received_open_queue_signal(self):
        """Display the header for the queue."""
        self._current_header.destroy()
        queue_header = ListHeader(self, "Queue")
        queue_header.grid(row=0, column=0, sticky="news")
        self._current_header = queue_header

    def received_open_playlists_signal(self):
        """Display the header for the opened playlist."""
        self._current_header.destroy()
        playlists_header = PlaylistsHeader(
            self, self._playlist_header_command
        )
        playlists_header.grid(row=0, column=0, sticky="news")
        self._current_header = playlists_header

    def _playlist_header_command(self, playlist_name):
        """Create a playlist with the given name."""
        self._music_database.create_playlist(playlist_name)
        self._sidebarframe.send_open_playlists_signal()

    def received_open_directories_signal(self):
        """Display the directory list header."""
        self._current_header.destroy()
        directories_header = DirectoriesHeader(
            self, self._directory_scan
        )
        directories_header.grid(row=0, column=0, sticky="news")
        self._current_header = directories_header
