import tkinter as tk
from functools import partial

from musicdatabase import MusicDatabase
from playbarframe import PlayBarFrame
from mixercontroller import MixerController
from tracklist import TrackList
from root import Root
from albumitem import AlbumItem
from frames import SideBarFrame
from trackitem import TrackItem
from artistitem import ArtistItem
from durationformat import format_duration

from root import BUTTON_COL, colour_scheme

# TRACK_LIST_COL = "#F6F7EB"
TRACK_LIST_COL = colour_scheme["grey"]


class TrackListFrame(tk.Frame):  # Displays the list of music tracks in a frame
    """
    Frame that contains the main display for music
    """
    def __init__(self, parent: Root, music_database: MusicDatabase, mixer_controller: MixerController, play_bar_frame: PlayBarFrame, track_list: TrackList, side_bar_frame: SideBarFrame):
        super().__init__()
        self.parent = parent  # Parent window (root window of the application)
        self.music_database = music_database  # track database performs database operations
        self.mixer_controller = mixer_controller
        self.track_list = track_list

        # Adds itself to listen to the navigation sidebar.
        side_bar_frame.open_album_list_observers.append(self)
        side_bar_frame.open_artist_list_observers.append(self)
        #side_bar_frame.open_song_list_observers.append(self)

        self.mixer_controller.new_track_observers.append(self)
        self.track_list.tracklist_updated_observers.append(self)  # Observes the tracklist and updates display when it changes

        self.play_track_observers = [mixer_controller, play_bar_frame]
        self.open_album_observers = [self.track_list]
        self.open_artist_page_observers = [self.track_list]

        # Initialise the Frame
        self.padding_size = self.parent.padding_size
        self.grid(row=1, column=1, sticky="news", padx=self.padding_size, pady=self.padding_size)
        self.config(width=740 - self.padding_size*2, height=300 - self.padding_size*2, bg=TRACK_LIST_COL)
        self._configure_grid()

        self.tracklist_frame, self.track_canvas = self.create_widgets()  # Create widgets and the frame to place track items on.

        self.track_items_dict = {}  # Dictionary of track_id's and the corresponding track item widgets
        self.album_list_dict = {}
        self.artist_list_dict = {}
        self.current_display_dict = None

        self.current_track = None

    def create_widgets(self):
        track_canvas = tk.Canvas(self)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=track_canvas.yview)
        tracklist_frame = tk.Frame(track_canvas, bg=TRACK_LIST_COL)
        tracklist_frame.grid_columnconfigure(0, weight=1)
        # <Configure> event triggers when the scrollable frame changes size.
        tracklist_frame.bind("<Configure>", self._on_frame_configure)
        track_canvas.bind("<Configure>", self._on_canvas_configure)

        track_canvas.configure(yscrollcommand=scrollbar.set, bg=TRACK_LIST_COL, highlightthickness=0)
        track_canvas.grid(row=0, column=0, sticky="news")

        track_canvas.create_window((0, 0), window=tracklist_frame, anchor="nw", tags=["track frame"])

        scrollbar.grid(row=0, column=1, sticky="news")

        return tracklist_frame, track_canvas

    def _on_frame_configure(self, event):
        # Update scroll region to encompass the size of the scrollable_frame
        self.track_canvas.configure(scrollregion=self.track_canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        # Update the width of the scrollable_frame to match the canvas width
        self.track_canvas.itemconfig("track frame", width=event.width)

    def received_tracklist_updated_signal(self):  # TrackListFrames listen for updated track lists.
        """
        Displays the updated tracklist
        """
        self.display_tracklist()

    def received_new_track_signal(self, track_id):
        """
        Method providing the display's response to a new track starting
        """
        self.update_highlighted_track(track_id)

    def update_highlighted_track(self, track_id):
        """
        Updates the currently highlighted track
        """
        print("Updating highlighted track to: ", track_id, "Current highlighted track is ", self.current_track)
        if self.current_track and self.current_track in self.track_items_dict:
            print(self.track_items_dict)
            track_to_remove_highlight = self.track_items_dict[self.current_track]
            print("Removing highlight for: ", track_to_remove_highlight)
            track_to_remove_highlight.remove_highlight()

        track_to_highlight = self.track_items_dict[track_id]
        track_to_highlight.add_highlight()
        self.current_track = track_id

    def _configure_grid(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def display_tracklist(self):
        """
        Updates the display to show the current tracklist
        """
        self.clear_display()

        tracks = self.track_list.tracklist  # Get the list of track IDs to display from the tracklist object
        tracks_info = self.music_database.get_track_metadata(tracks)
        track_number = 1

        # Create a track item widget for each track in the list.
        for track_id in tracks:
            track_info = tracks_info[track_id]  # tracks_info is a dictionary pairing the track_id with its metadata
            self.create_track_item(track_id, track_info, track_number)
            track_number += 1
            # Highlight the track item if it's currently playing
            if track_id == self.mixer_controller.current_track_id:
                self.update_highlighted_track(track_id)

        self.current_display_dict = self.track_items_dict  #

        self.track_canvas.yview_moveto(0)  # Moves to the top of the scrollable canvas.

    def create_track_item(self, track_id, track_info, track_number):
        """
        Creates an instance of the TrackItems class for a given track
        """
        track_name = track_info['track_name']
        print(track_id, track_name)
        artist_id = track_info['artist']
        artist_name = self.music_database.get_artist_name(artist_id)
        album_id = track_info['album']
        album = self.music_database.get_album_title(album_id)

        duration_full = track_info['duration']
        duration = format_duration(duration_full)

        release_date = track_info['release_date']
        play_command = partial(self.send_play_track_signal, track_id)  # The command passed to the TrackItem buttons

        track_item = TrackItem(
            self.tracklist_frame,
            play_command=play_command,
            track_name=track_name,
            artist_name=artist_name,
            artist_id=artist_id,
            album=album,
            album_id=album_id,
            release_date=release_date,
            track_number=track_number,
            duration=duration
        )
        track_item.grid(row=track_number-1)

        self.track_items_dict[track_id] = track_item

    def send_play_track_signal(self, song_id):
        """
        Signals that the user has requested to play a track
        """
        print("User request to play song with id: ", song_id)
        print("Sending play track signal to observers: ", self.play_track_observers)
        for listener in self.play_track_observers:
            listener.received_play_track_signal(song_id)

    def display_album_list(self):
        """
        Displays a list of all albums
        """
        self.clear_display()

        album_list = self.music_database.get_all_albums()
        albums_info = self.music_database.get_album_metadata(album_list)
        for album in album_list:
            info = albums_info[album]
            self.create_album_item(album, info)

        self.current_display_dict = self.album_list_dict

        self.track_canvas.yview_moveto(0)  # Moves to the top of the scrollable canvas.

    def create_album_item(self, album_id, album_info):
        """
        Creates an instance of the AlbumItems class for a given album
        """
        album_name = album_info["album_name"]
        artist_id = album_info["artist_id"]
        artist_name = album_info["artist_name"]
        release_date = album_info["release_date"]
        open_album_command = partial(self.send_open_album_signal, album_id, album_name)

        album = AlbumItem(
            self.tracklist_frame,
            album_id=album_id,
            album_name=album_name,
            artist_id=artist_id,
            artist_name=artist_name,
            release_date=release_date,
            open_album_command=open_album_command
        )
        album.grid(column=0, sticky="news", pady=5, padx=10)

        self.album_list_dict[album_id] = album

    def send_open_album_signal(self, album_id, album_name):
        """
        Signals that the user requested to open an album
        """
        print("Opening album: ", album_id, album_name)
        for observer in self.open_album_observers:
            observer.received_open_album_signal(album_id)
        return

    def clear_display(self):
        """
        Removes all widgets on the current display
        """
        if self.current_display_dict:
            for widget_id in self.current_display_dict:
                self.current_display_dict[widget_id].destroy()
            self.track_items_dict = {}
            self.album_list_dict = {}
            self.artist_list_dict = {}

    def display_artist_list(self):
        """
        Displays a list of all artists in the database
        """
        self.clear_display()

        artist_list = self.music_database.get_all_artists()
        artist_info = self.music_database.get_artist_metadata(artist_list)

        for artist_id in artist_list:
            info = artist_info[artist_id]
            self.create_artist_item(artist_id, info)

        self.current_display_dict = self.artist_list_dict

        self.track_canvas.yview_moveto(0)  # Moves to the top of the scrollable canvas.

    def create_artist_item(self, artist_id, artist_info):
        """
        Creates an instance of the ArtistItem class for the given artist
        """
        artist_name = artist_info["artist_name"]
        open_artist_page_command = partial(self.send_open_artist_page_signal, artist_id)

        artist = ArtistItem(self.tracklist_frame, artist_name, open_artist_page_command)
        artist.grid(column=0, sticky="news", pady=5, padx=10)

        self.artist_list_dict[artist_id] = artist

    def send_open_artist_page_signal(self, artist_id):
        """
        Signals that the user wants to open an artist's page
        """
        for observer in self.open_artist_page_observers:
            observer.received_open_artist_page_signal(artist_id)

    def received_open_album_list_signal(self):
        """
        Responds to the signal to open the list of albums
        """
        self.display_album_list()

    def received_open_artist_list_signal(self):
        """
        Responds to the signal to open the list of artists
        """
        self.display_artist_list()


