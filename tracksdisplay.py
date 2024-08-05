from functools import partial

from musicdatabase import MusicDatabase
from durationformat import format_duration
from trackitem import TrackItem
from tracklist import TrackList
from mixercontroller import MixerController

from root import BUTTON_COL, colour_scheme


TRACK_LIST_COL = colour_scheme["grey"]


class TracksDisplay:
    def __init__(self, display_frame, display_canvas,
                 music_database: MusicDatabase,
                 track_list: TrackList,
                 mixer_controller: MixerController,
                 play_track_function, add_to_queue_function):
        self.display_frame = display_frame
        self.display_canvas = display_canvas
        self.music_database = music_database
        self.track_list = track_list
        self.mixer_controller = mixer_controller

        self.play_track_function = play_track_function
        self.add_to_queue_function = add_to_queue_function

        self.track_items_dict = {}
        self.highlighted_track = None

    def display_tracklist(self):
        """
        Updates the display to show the current tracklist
        """
        self.clear_display()
        # Get the list of track IDs to display from the tracklist object
        tracks = self.track_list.tracklist
        tracks_info = self.music_database.get_track_metadata(tracks)
        track_number = 1

        # Create a track item widget for each track in the list.
        for track_id in tracks:
            # tracks_info is a dictionary pairing the track_id with its metadata
            track_info = tracks_info[track_id]
            self.create_track_item(track_id, track_info, track_number)
            track_number += 1
            # Highlight the track item if it's currently playing
            if track_id == self.mixer_controller.current_track_id:
                self.update_highlighted_track(track_id)

        # Move to the top of the scrollable canvas.
        self.display_canvas.yview_moveto(0)

    def create_track_item(self, track_id, track_info, track_number):
        """
        Creates an instance of the TrackItems class for a given track
        """
        track_name = track_info['track_name']
        artist_id = track_info['artist']
        artist_name = self.music_database.get_artist_name(artist_id)
        album_id = track_info['album']
        album = self.music_database.get_album_title(album_id)
        duration_full = track_info['duration']
        duration = format_duration(duration_full)
        release_date = track_info['release_date']
        play_command = partial(self.play_track_function, track_id)
        add_to_queue_command = partial(self.add_to_queue_function, track_id)

        track_item = TrackItem(
            self.display_frame,
            play_command=play_command,
            track_name=track_name,
            artist_name=artist_name,
            artist_id=artist_id,
            album=album,
            album_id=album_id,
            release_date=release_date,
            track_number=track_number,
            duration=duration,
            add_to_queue_command=add_to_queue_command
        )
        track_item.grid(row=track_number - 1, column=0,
                        sticky="news", pady=5, padx=10)

        self.track_items_dict[track_id] = track_item

    def clear_display(self):
        """
        Removes all widgets on the current display
        """
        for track_item_id in self.track_items_dict:
            self.track_items_dict[track_item_id].destroy()

        self.track_items_dict = {}

    def update_highlighted_track(self, track_id):
        """
        Updates the currently highlighted track
        """
        # Check if the previously highlighted track needs the highlight
        # removed as it may have already been destroyed
        if (self.highlighted_track
                and self.highlighted_track in self.track_items_dict):
            track_to_remove_highlight = self.track_items_dict[self.highlighted_track]
            track_to_remove_highlight.remove_highlight()

        # Update the new track if it's currently being displayed
        if self.track_items_dict and track_id in self.track_items_dict:
            track_to_highlight = self.track_items_dict[track_id]
            track_to_highlight.add_highlight()
            self.highlighted_track = track_id
