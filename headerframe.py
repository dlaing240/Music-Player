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


HEADER_COL = colour_scheme["grey"]


class HeaderFrame(tk.Frame):
    """
    Class to provide the header for the application
    """
    def __init__(self, parent: Root,
                 tracklist: TrackList,
                 mixer_controller: MixerController,
                 music_database: MusicDatabase,
                 sidebarframe: SideBarFrame,
                 directory_scan: DirectoryScan):
        super().__init__(parent)
        self.parent = parent
        self.tracklist = tracklist
        self.mixer_controller = mixer_controller
        self.music_database = music_database
        self.sidebarframe = sidebarframe
        self.directory_scan = directory_scan

        # listen for updates to the display
        self.tracklist.tracklist_updated_observers.append(self)
        self.sidebarframe.open_artist_list_observers.append(self)
        self.sidebarframe.open_album_list_observers.append(self)
        self.sidebarframe.open_queue_observers.append(self)
        self.sidebarframe.open_playlist_observers.append(self)
        self.sidebarframe.open_directories_observers.append(self)

        self.update_playlist_display_observers = []

        self.padding_size = self.parent.padding_size
        self.grid(row=0, column=1, sticky="news",
                  padx=self.padding_size, pady=self.padding_size)
        self.config(width=640 - self.padding_size*2,
                    height=100 - self.padding_size*2, bg=HEADER_COL)
        self._grid_config()

        self.current_header = None
        self.display_collection_header()

    def _grid_config(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def display_collection_header(self):
        collection_type = self.tracklist.collection_type
        collection_id = self.tracklist.collection_id
        collection_title = self.tracklist.collection_title
        track_count = len(self.tracklist.get_tracklist())
        duration = self.tracklist.get_total_tracklist_duration()
        if collection_type == "album":
            artist_id = self.music_database.get_album_metadata(
                [collection_id]
            )[collection_id]["artist_id"]
            subtitle = self.music_database.get_artist_name(artist_id)
        else:
            subtitle = None

        collections_header = CollectionsHeader(
            parent=self,
            play_all_command=self.mixer_controller.play_all,
            collection_type=collection_type,
            collection_title=collection_title,
            collection_id=collection_id,
            track_count=track_count,
            duration=duration,
            subtitle=subtitle
        )

        collections_header.grid(row=0, column=0, sticky="news")
        self.current_header = collections_header

    def received_tracklist_updated_signal(self):
        self.current_header.destroy()
        self.display_collection_header()

    def received_open_album_list_signal(self):
        self.current_header.destroy()
        album_list_header = ListHeader(self, "Albums")
        album_list_header.grid(row=0, column=0,  sticky="news")
        self.current_header = album_list_header

    def received_open_artist_list_signal(self):
        self.current_header.destroy()
        artist_list_header = ListHeader(self, "Artists")
        artist_list_header.grid(row=0, column=0, sticky="news")
        self.current_header = artist_list_header

    def received_open_queue_signal(self):
        self.current_header.destroy()
        queue_header = ListHeader(self, "Queue")
        queue_header.grid(row=0, column=0, sticky="news")
        self.current_header = queue_header

    def received_open_playlists_signal(self):
        self.current_header.destroy()
        playlists_header = PlaylistsHeader(
            self, self.playlist_header_command
        )
        playlists_header.grid(row=0, column=0, sticky="news")
        self.current_header = playlists_header

    def playlist_header_command(self, playlist_name):
        """
        Method used to create a playlist via a button on the
        playlist header frame

        Parameters
        ----------
        playlist_name

        Returns
        -------

        """
        self.music_database.create_playlist(playlist_name)
        self.sidebarframe.send_open_playlists_signal()

    def received_open_directories_signal(self):
        """
        Method to display the directories header

        Returns
        -------

        """
        self.current_header.destroy()
        directories_header = DirectoriesHeader(
            self, self.directory_scan
        )
        directories_header.grid(row=0, column=0, sticky="news")
        self.current_header = directories_header
