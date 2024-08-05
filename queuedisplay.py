import tkinter as tk
from functools import partial

from mixercontroller import MixerController
from musicdatabase import MusicDatabase
from queueitem import QueueItem
from durationformat import format_duration


class QueueDisplay:
    def __init__(self, mixer_controller: MixerController,
                 music_database: MusicDatabase, display_canvas,
                 display_frame, play_track_function, add_to_queue_function):
        self.mixer_controller = mixer_controller
        self.music_database = music_database
        self.display_canvas = display_canvas
        self.display_frame = display_frame
        self.play_track_function = play_track_function
        self.add_to_queue_function = add_to_queue_function

        self.highlighted_track = None
        self.queue_items_dict = {}
        self.queue_index = 0
        self.queue_id = 0
        self.max_queue_index = len(self.mixer_controller.active_queue) - 1
        self.is_displayed = False

    def display_queue(self):
        self.clear_display()
        queue = self.mixer_controller.active_queue
        self.max_queue_index = len(queue) - 1
        tracks_info = self.music_database.get_track_metadata(queue)
        self.queue_index = 0

        for track_id in queue:
            track_info = tracks_info[track_id]
            self.create_queue_item(track_id, track_info,
                                   self.queue_index, self.max_queue_index)
            self.queue_index += 1
            if track_id == self.mixer_controller.current_track_id:
                self.update_highlighted_track()

        self.display_canvas.yview_moveto(0)
        self.is_displayed = True

    def create_queue_item(self, track_id, track_info, queue_index, queue_max):
        track_name = track_info['track_name']
        artist_id = track_info['artist']
        artist_name = self.music_database.get_artist_name(artist_id)
        album_id = track_info['album']
        album = self.music_database.get_album_title(album_id)
        duration_full = track_info['duration']
        duration = format_duration(duration_full)
        release_date = track_info['release_date']
        # Pass the play button command to the QueueItem
        play_command = partial(self.play_track_function, track_id)
        add_to_queue_command = partial(self.add_to_queue_function, track_id)

        queue_item = QueueItem(
            self.display_frame,
            play_command=play_command,
            track_name=track_name,
            artist_name=artist_name,
            artist_id=artist_id,
            album=album,
            album_id=album_id,
            release_date=release_date,
            track_number=queue_index + 1,
            duration=duration,
            queue_index=queue_index,
            reorder_queue_function=self.reorder_queue,
            track_id=track_id,
            queue_max=queue_max,
            add_to_queue_command=add_to_queue_command
        )
        queue_item.grid(row=queue_index, column=0,
                        sticky="news", pady=5, padx=10)

        self.queue_items_dict[self.queue_index] = queue_item

    def reorder_queue(self, old_index, new_index, track_id):
        # Reorder the mixer queue
        self.mixer_controller.reorder_queue(old_index, new_index, track_id)
        moved_item = self.queue_items_dict[old_index]  # The item to be moved
        replacement_item = self.queue_items_dict[new_index]  # The item currently in the target position
        # swap keys in the dictionary
        self.queue_items_dict[new_index] = moved_item
        self.queue_items_dict[old_index] = replacement_item

        # Change the moved items' rows
        moved_item.grid(row=new_index, column=0,
                        sticky="news", pady=5, padx=10)
        replacement_item.grid(row=old_index, column=0,
                              sticky="news", pady=5, padx=10)
        replacement_item.queue_index = old_index
        replacement_item.update_track_number()

        if moved_item.is_highlighted:
            self.highlighted_track = new_index
        elif replacement_item.is_highlighted:
            self.highlighted_track = old_index

    def clear_display(self):
        """
        Removes all widgets on the current display
        """
        for track_item_id in self.queue_items_dict:
            self.queue_items_dict[track_item_id].destroy()

        self.queue_items_dict = {}

    def update_highlighted_track(self):
        """
        Updates the currently highlighted track
        """
        # First, check if the previously highlighted track needs the highlight removed
        # as it may have already been destroyed
        if (self.highlighted_track is not None
                and self.highlighted_track in self.queue_items_dict):
            track_widget = self.queue_items_dict[self.highlighted_track]
            track_widget.remove_highlight()

        # The dictionary of queue items uses the track's position in the queue as its key
        currently_playing_pos = self.mixer_controller.pos_in_queue

        # Update the new track if it's currently being displayed
        if (self.queue_items_dict
                and currently_playing_pos in self.queue_items_dict):
            track_to_highlight = self.queue_items_dict[currently_playing_pos]
            track_to_highlight.add_highlight()
            self.highlighted_track = currently_playing_pos

    def received_add_to_queue_signal(self, track_id):
        pass
