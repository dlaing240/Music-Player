import tkinter as tk

from musicdatabase import MusicDatabase
from playbarframe import PlayBarFrame
from mixercontroller import MixerController
from tracklist import TrackList
from root import Root
from sidebarframe import SideBarFrame
from tracksdisplay import TracksDisplay
from albumsdisplay import AlbumsDisplay
from artistdisplay import ArtistsDisplay
from queuedisplay import QueueDisplay
from allplaylistsdisplay import AllPlaylistsDisplay
from playlistdisplay import PlaylistDisplay
from directoriesdisplay import DirectoriesDisplay
from scandirectory import DirectoryScan
from headerframe import HeaderFrame

from root import BUTTON_COL, colour_scheme

TRACK_LIST_COL = colour_scheme["grey"]


class TrackListFrame(tk.Frame):
    """
    Frame that contains the main display for music
    """
    def __init__(self, parent: Root,
                 music_database: MusicDatabase,
                 mixer_controller: MixerController,
                 play_bar_frame: PlayBarFrame,
                 track_list: TrackList,
                 side_bar_frame: SideBarFrame,
                 directory_scan: DirectoryScan,
                 header_frame: HeaderFrame):
        super().__init__()
        self.parent = parent  # Parent window (root window of the application)
        # track database performs database operations
        self.music_database = music_database
        self.mixer_controller = mixer_controller
        self.track_list = track_list
        self.side_bar_frame = side_bar_frame

        # Adds itself to listen to the navigation sidebar.
        side_bar_frame.open_album_list_observers.append(self)
        side_bar_frame.open_artist_list_observers.append(self)
        side_bar_frame.open_queue_observers.append(self)
        side_bar_frame.open_playlist_observers.append(self)
        side_bar_frame.open_directories_observers.append(self)
        #side_bar_frame.open_song_list_observers.append(self)

        header_frame.update_playlist_display_observers.append(self)

        self.mixer_controller.new_track_observers.append(self)
        # Observes the tracklist and updates display when it changes
        self.track_list.tracklist_updated_observers.append(self)

        # Initialise the Frame
        self.padding_size = self.parent.padding_size
        self.grid(row=1, column=1, sticky="news",
                  padx=self.padding_size, pady=self.padding_size)
        self.config(width=740 - self.padding_size*2,
                    height=300 - self.padding_size*2, bg=TRACK_LIST_COL)
        self._configure_grid()

        # Create widgets and the frame to place items on.
        self.display_frame, self.display_canvas = self.create_widgets()

        # Create displays
        self.track_display = TracksDisplay(
            self.display_frame,
            self.display_canvas,
            self.music_database,
            self.track_list,
            self.mixer_controller,
            self.send_play_track_signal,
            self.send_add_to_queue_signal,
            self.send_play_next_signal,
            go_to_directories_fn=self.go_to_directories
        )
        self.playlist_display = PlaylistDisplay(self.display_frame,
                                                self.display_canvas,
                                                self.music_database,
                                                self.track_list,
                                                self.mixer_controller,
                                                self.send_play_track_signal,
                                                self.send_add_to_queue_signal,
                                                self.send_play_next_signal)

        self.albums_display = AlbumsDisplay(self.display_frame,
                                            self.display_canvas,
                                            self.music_database,
                                            self.send_open_album_signal)
        self.artist_display = ArtistsDisplay(self.display_frame,
                                             self.display_canvas,
                                             self.music_database,
                                             self.send_open_artist_page_signal)
        self.queue_display = QueueDisplay(self.display_frame,
                                          self.display_canvas,
                                          self.music_database,
                                          self.track_list,
                                          self.mixer_controller,
                                          self.send_play_track_signal,
                                          self.send_add_to_queue_signal,
                                          self.send_play_next_signal)
        self.all_playlists_display = AllPlaylistsDisplay(self.display_frame,
                                                         self.display_canvas,
                                                         self.music_database,
                                                         self.send_open_playlist_signal)
        self.directories_display = DirectoriesDisplay(directory_scan, self.display_frame)

        self.displays_with_tracks = {self.track_display,
                                     self.queue_display,
                                     self.playlist_display}

        # Establish lists of observers to the signals sent by this frame
        self.play_track_observers = [mixer_controller, play_bar_frame]
        self.open_album_observers = [self.track_list]
        self.open_artist_page_observers = [self.track_list]
        self.add_to_queue_observers = [self.mixer_controller,
                                       self.queue_display]
        self.open_playlist_observers = [self.track_list]
        self.play_next_observers = [mixer_controller]

        self.current_display = self.track_display

    def _configure_grid(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def create_widgets(self):
        display_canvas = tk.Canvas(self)
        scrollbar = tk.Scrollbar(self, orient="vertical",
                                 command=display_canvas.yview)
        display_frame = tk.Frame(display_canvas, bg=TRACK_LIST_COL)
        display_frame.grid_columnconfigure(0, weight=1)
        #display_frame.grid_columnconfigure(1, weight=1)
        # <Configure> event triggers when the scrollable frame changes size.
        display_frame.bind("<Configure>", self._on_frame_configure)
        display_canvas.bind("<Configure>", self._on_canvas_configure)
        display_canvas.configure(yscrollcommand=scrollbar.set,
                                 bg=TRACK_LIST_COL, highlightthickness=0)
        display_canvas.grid(row=0, column=0, sticky="news")
        display_canvas.create_window((0, 0), window=display_frame,
                                     anchor="nw", tags=["track frame"])
        display_canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        scrollbar.grid(row=0, column=1, sticky="news")

        return display_frame, display_canvas

    def _on_frame_configure(self, event):
        # Update scroll region to encompass the size of the scrollable_frame
        self.display_canvas.configure(
            scrollregion=self.display_canvas.bbox("all")
        )

    def _on_canvas_configure(self, event):
        # Update the width of the scrollable_frame to match the canvas width
        self.display_canvas.itemconfig("track frame", width=event.width)

    def _on_mousewheel(self, event):
        self.display_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def clear_display(self):
        """
        Removes all widgets on the current display
        """
        # self.artist_display.clear_display()
        # self.track_display.clear_display()
        # self.albums_display.clear_display()
        # self.queue_display.clear_display()
        # self.all_playlists_display.clear_display()
        # self.playlist_display.clear_display()
        # self.directories_display.clear_display()
        #
        # self.ball_display.clear_display()
        self.current_display.clear_display()

    def received_tracklist_updated_signal(self):  # TrackListFrames listen for updated track lists.
        """
        Displays the updated tracklist
        """
        self.clear_display()
        if self.track_list.collection_type == "playlist":
            playlist_id = self.track_list.collection_id
            self.playlist_display.display_collection(playlist_id)
            self.current_display = self.playlist_display
        else:
            self.track_display.display_tracklist()
            self.current_display = self.track_display

    def received_open_album_list_signal(self):
        """
        Responds to the signal to open the list of albums
        """
        self.clear_display()
        self.albums_display.display_album_list()
        self.current_display = self.albums_display

    def received_open_artist_list_signal(self):
        """
        Responds to the signal to open the list of artists
        """
        self.clear_display()
        self.artist_display.display_artist_list()
        self.current_display = self.artist_display

    def received_open_queue_signal(self):
        """
        Responds to the signal to open the queue
        """
        self.clear_display()
        self.queue_display.display_queue()
        self.current_display = self.queue_display

        # the tracklist is kept separate from the queue
        self.track_list.has_changed = False

    def received_open_playlists_signal(self):
        """
        Opens the playlists display

        Returns
        -------

        """
        self.clear_display()
        self.all_playlists_display.display_playlist_list()
        self.current_display = self.all_playlists_display

    def go_to_directories(self):
        self.side_bar_frame.send_open_directories_signal()

    def received_open_directories_signal(self):
        """
        Opens the directories display

        Returns
        -------

        """
        self.clear_display()
        self.directories_display.display()
        self.current_display = self.directories_display

    def received_new_track_signal(self, track_id):
        """
        Method providing the display's response to a new track starting
        """
        if self.current_display in self.displays_with_tracks:
            self.current_display.update_highlighted_track(track_id)

    def send_play_track_signal(self, song_id):
        """
        Signals that the user has requested to play a track
        """
        for listener in self.play_track_observers:
            listener.received_play_track_signal(song_id)

    def send_open_album_signal(self, album_id, album_name):
        """
        Signals that the user requested to open an album
        """
        for observer in self.open_album_observers:
            observer.received_open_album_signal(album_id)
        return

    def send_open_artist_page_signal(self, artist_id):
        """
        Signals that the user wants to open an artist's page
        """
        for observer in self.open_artist_page_observers:
            observer.received_open_artist_page_signal(artist_id)

    def send_open_playlist_signal(self, playlist_id):
        """
        Signals that a playlist has been opened

        Parameters
        ----------
        playlist_id

        Returns
        -------

        """
        for observer in self.open_playlist_observers:
            observer.received_open_playlist_signal(playlist_id)

    def send_add_to_queue_signal(self, track_id):
        """
        Signals that a track is to be added to the queue
        """
        for observer in self.add_to_queue_observers:
            observer.received_add_to_queue_signal(track_id)

    def send_play_next_signal(self, track_id):
        """
        Signals that a track needs to be played next
        Parameters
        ----------
        track_id

        Returns
        -------

        """
        for observer in self.play_next_observers:
            observer.received_play_next_signal(track_id)

    def received_update_playlist_display_signal(self):
        self.all_playlists_display.display_playlist_list()
