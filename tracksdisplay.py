from functools import partial
import tkinter as tk

from musicdatabase import MusicDatabase
from durationformat import format_duration
from trackitem import TrackItem
from tracklist import TrackList
from mixercontroller import MixerController

from root import BUTTON_COL, colour_scheme, BATTLESHIP_GREY


TRACK_LIST_COL = colour_scheme["grey"]


class TracksDisplay:
    def __init__(self, display_frame, display_canvas,
                 music_database: MusicDatabase,
                 track_list: TrackList,
                 mixer_controller: MixerController,
                 play_track_function, add_to_queue_function,
                 play_next_function, go_to_directories_fn=None):
        self.display_frame = display_frame
        self.display_canvas = display_canvas
        self.music_db = music_database
        self.track_list = track_list
        self.mixer_controller = mixer_controller

        self.play_track_function = play_track_function
        self.play_next_function = play_next_function
        self.add_to_queue_function = add_to_queue_function
        self.go_to_directories_fn = go_to_directories_fn

        self.start_column = 0

        self.widgets_dict = {}  # Maps track widgets to their widget_ids
        self.all_track_widgets = []
        self.highlighted_track = None
        self.empty_display_widgets = []

    def display_tracklist(self):
        """
        Updates the display to show the current tracklist
        """
        self.clear_display()
        tracks = self.get_tracks()
        tracks_info = self.music_db.get_track_metadata(tracks)
        widget_ids = self.get_widget_ids(tracks)
        track_number = 1

        for track_id, widget_id in zip(tracks, widget_ids):
            track_info = tracks_info[track_id]
            self.create_track_item(track_id, track_info, track_number, widget_id)
            track_number += 1
            # Highlight the track item if it's currently playing
            if track_id == self.mixer_controller.current_track_id:
                self.update_highlighted_track(track_id)

        # Move to the top of the scrollable canvas.
        self.display_canvas.yview_moveto(0)

        if not self.widgets_dict:
            self.empty_tracklist()

    def get_tracks(self):
        """
        Gets the list of track_ids from the tracklist

        Returns
        -------

        """
        return self.track_list.tracklist

    def get_widget_ids(self, tracks):
        """
        Gives a list of unique widget_ids from a list of tracks

        Parameters
        ----------
        tracks

        Returns
        -------

        """
        # In the case of the tracks display, track_id is also used for the
        # widget id.
        return tracks

    def create_track_item(self, track_id, track_info, track_number, widget_id):
        """
        Creates an instance of the TrackItems class for a given track
        """
        track_name = track_info['track_name']
        artist_id = track_info['artist']
        artist_name = self.music_db.get_artist_name(artist_id)
        album_id = track_info['album']
        album = self.music_db.get_album_title(album_id)
        duration_full = track_info['duration']
        duration = format_duration(duration_full)
        release_date = track_info['release_date']

        play_next_command = partial(self.play_next_function, track_id)
        add_to_queue_command = partial(self.add_to_queue_function, track_id)
        add_to_playlist_command = partial(
            self.music_db.add_to_playlist, track_id
        )

        playlists_data = self.music_db.get_playlists()
        playlists = [(playlist_id, playlists_data[playlist_id]) for playlist_id in playlists_data]

        track_item = TrackItem(
            self.display_frame,
            play_command=lambda t: self.on_play_press(t),
            track_id=track_id,
            track_name=track_name,
            artist_name=artist_name,
            artist_id=artist_id,
            album=album,
            album_id=album_id,
            release_date=release_date,
            track_number=track_number,
            duration=duration,
            add_to_queue_command=add_to_queue_command,
            add_to_playlist_command=add_to_playlist_command,
            play_next_command=play_next_command,
            playlists=playlists,
            create_new_playlist_command=self.music_db.create_playlist,
            start_column=self.start_column
        )
        track_item.grid(row=track_number - 1, column=0,
                        sticky="news", pady=5, padx=10)

        self.widgets_dict[track_id] = track_item
        self.all_track_widgets.append(track_item)

    def on_play_press(self, track_item):
        """
        Method called when the track's play button is pressed

        Parameters
        ----------
        track_item

        Returns
        -------

        """
        track_id = track_item.track_id
        self.play_track_function(track_id)

    def clear_display(self):
        """
        Removes all widgets on the current display
        """
        for track_item_id in self.widgets_dict:
            self.widgets_dict[track_item_id].destroy()

        self.widgets_dict = {}
        self.all_track_widgets = []
        for widget in self.empty_display_widgets:
            widget.destroy()
        self.empty_display_widgets = []
        self.highlighted_track = None

    def update_highlighted_track(self, track_id):
        """
        Updates the currently highlighted track
        """
        # Check if the previously highlighted track needs the highlight
        # removed as it may have already been destroyed
        if (self.highlighted_track
                and self.highlighted_track in self.widgets_dict):
            track_to_remove_highlight = self.widgets_dict[self.highlighted_track]
            track_to_remove_highlight.remove_highlight()

        # Update the new track if it's currently being displayed
        if self.widgets_dict and track_id in self.widgets_dict:
            track_to_highlight = self.widgets_dict[track_id]
            track_to_highlight.add_highlight()
            self.highlighted_track = track_id

    def empty_tracklist(self):
        """
        Displays the empty tracklist message

        Returns
        -------

        """
        empty_display_text = tk.Label(
            self.display_frame,
            text='''"Without music, life would be a mistake"
            \n-Friedrich Nietzsche
            \n(I think you should add some music...)
            ''',
            bg=colour_scheme["grey"],
            fg=BATTLESHIP_GREY,
            font=("Arial", 20),
        )
        empty_display_text.grid(row=0, column=0, sticky="news")

        button = tk.Button(
            self.display_frame,
            text="➕ Add Music",
            font=("Ariel", 16),
            command=self.go_to_directories_fn,
            width=11,
            fg="white",
            bg=colour_scheme["grey"],
            highlightthickness=0,
            relief="flat",
            anchor="w"
        )
        button.grid(row=1, column=0, padx=10, pady=5)
        self.empty_display_widgets = [empty_display_text, button]
