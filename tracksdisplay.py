from functools import partial
import tkinter as tk

from musicdatabase import MusicDatabase
from durationformat import format_duration
from trackitem import TrackItem
from tracklist import TrackList
from mixercontroller import MixerController

from root import colour_scheme


class TracksDisplay:
    """
    Class to display a list of tracks.

    Attributes
    ----------
    widgets_dict : dict
        Maps track widgets to their widget_ids.
    all_track_widgets : list
        List containing all created widgets.
    highlighted_track : int
        The `track_id` of currently highlighted track.
    empty_display_widgets : list
        List for the widgets created for empty displays.

    Methods
    -------
    display_tracklist():
        Display the current tracklist.
    clear_display():
        Remove all widgets on the current display.
    update_highlighted_track(track_id):
        Update the currently highlighted track.
    """

    def __init__(self, display_frame, display_canvas,
                 music_database: MusicDatabase,
                 track_list: TrackList,
                 mixer_controller: MixerController,
                 play_track_function, add_to_queue_function,
                 play_next_function, go_to_directories_fn=None):
        """
        Initialise a `TracksDisplay` instance.

        Parameters
        ----------
        display_frame : tkinter.Frame
            The frame to place playlist widgets on.
        display_canvas : tkinter.Canvas
            The canvas containing the `display_frame`.
        music_database : MusicDatabase
            Instance of `MusicDatabase`.
        track_list : TrackList
            Instance of `TrackList`.
        mixer_controller : MixerController.
            Instance of `MixerController`.
        play_track_function : callable
            Method called when a play button is pressed.
        add_to_queue_function : callable
            Method called when the `add_to_queue` menu option is pressed.
        play_next_function : callable
            Method called when the `play_next` menu option is pressed.
        go_to_directories_fn : callable
            Method to navigate to the directories display.
        """
        self.display_frame = display_frame
        self.display_canvas = display_canvas
        self._music_db = music_database
        self._track_list = track_list
        self._mixer_controller = mixer_controller
        self._colour_scheme = colour_scheme

        self._play_track_function = play_track_function
        self._play_next_function = play_next_function
        self._add_to_queue_function = add_to_queue_function
        self._go_to_directories_fn = go_to_directories_fn

        self._start_column = 0

        self.widgets_dict = {}  # Maps track widgets to their widget_ids
        self.all_track_widgets = []
        self.highlighted_track = None
        self.empty_display_widgets = []

    def _get_tracks(self):
        """Return the list of `track_id`s from the tracklist"""
        return self._track_list.tracklist

    def _get_widget_ids(self, tracks):
        """
        Return a list of unique widget_ids from a list of tracks.

        In the case of the tracks display, track_id is also used for the
        widget id
        """
        return tracks

    def _on_play_press(self, track_item):
        """Play a track from its `track_item`."""
        track_id = track_item.track_id
        self._play_track_function(track_id)

    def display_tracklist(self):
        """Display the current tracklist."""
        self.clear_display()
        tracks = self._get_tracks()
        tracks_info = self._music_db.get_track_metadata(tracks)
        widget_ids = self._get_widget_ids(tracks)
        track_number = 1

        for track_id, widget_id in zip(tracks, widget_ids):
            track_info = tracks_info[track_id]
            self._create_track_item(track_id, track_info, track_number)
            track_number += 1
            # Highlight the track item if it's currently playing
            if track_id == self._mixer_controller.current_track_id:
                self.update_highlighted_track(track_id)

        # Move to the top of the scrollable canvas.
        self.display_canvas.yview_moveto(0)

        if not self.widgets_dict:
            self._empty_tracklist()

    def _create_track_item(self, track_id, track_info, track_number):
        """Create a `TrackItem` instance for a given track."""
        track_name = track_info['track_name']
        artist_id = track_info['artist']
        artist_name = self._music_db.get_artist_name(artist_id)
        album_id = track_info['album']
        album = self._music_db.get_album_title(album_id)
        duration_full = track_info['duration']
        duration = format_duration(duration_full)
        release_date = track_info['release_date']

        play_next_command = partial(self._play_next_function, track_id)
        add_to_queue_command = partial(self._add_to_queue_function, track_id)
        add_to_playlist_command = partial(
            self._music_db.add_to_playlist, track_id
        )

        playlists_data = self._music_db.get_playlists()
        playlists = [(playlist_id, playlists_data[playlist_id]) for playlist_id in playlists_data]

        track_item = TrackItem(
            self.display_frame,
            play_command=lambda t: self._on_play_press(t),
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
            create_new_playlist_command=self._music_db.create_playlist,
            start_column=self._start_column
        )
        track_item.grid(row=track_number - 1, column=0,
                        sticky="news", pady=5, padx=10)

        self.widgets_dict[track_id] = track_item
        self.all_track_widgets.append(track_item)

    def _empty_tracklist(self):
        """Display the empty tracklist widgets."""
        empty_display_text = tk.Label(
            self.display_frame,
            text='''"Without music, life would be a mistake"
            \n-Friedrich Nietzsche
            \n(I think you should add some music...)
            ''',
            bg=self._colour_scheme["grey"],
            fg=self._colour_scheme["battleship"],
            font=("Arial", 20),
        )
        empty_display_text.grid(row=0, column=0, sticky="news")

        self.empty_display_widgets.append(empty_display_text)

        if self._go_to_directories_fn:
            button = tk.Button(
                self.display_frame,
                text="➕ Add Music",
                font=("Ariel", 16),
                command=self._go_to_directories_fn,
                width=11,
                fg="white",
                bg=self._colour_scheme["grey"],
                highlightthickness=0,
                relief="flat",
                anchor="w"
            )
            button.grid(row=1, column=0, padx=10, pady=5)
            self.empty_display_widgets.append(button)

    def clear_display(self):
        """Remove all widgets on the current display."""
        for track_item_id in self.widgets_dict:
            self.widgets_dict[track_item_id].destroy()

        self.widgets_dict = {}
        self.all_track_widgets = []
        for widget in self.empty_display_widgets:
            widget.destroy()
        self.empty_display_widgets = []
        self.highlighted_track = None

    def update_highlighted_track(self, track_id):
        """Update the currently highlighted track."""
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
