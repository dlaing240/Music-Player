import tkinter as tk
import numpy as np

from tracksdisplay import TracksDisplay

from root import colour_scheme


class QueueDisplay(TracksDisplay):
    """
    Class to display the music queue.

    Methods
    -------
    clear_display():
        Destroy all the displayed widgets.
        Overwrites `TracksDisplay.clear_display()`.
    display_queue():
        Create and display the queue display.
    """
    def __init__(self, display_frame, display_canvas, music_database,
                 track_list, mixer_controller, play_track_function,
                 add_to_queue_function, play_next_function):
        """
        Initialise a `QueueDisplay` instance.

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
        """
        super().__init__(display_frame, display_canvas, music_database,
                         track_list, mixer_controller, play_track_function,
                         add_to_queue_function, play_next_function)
        self._pos_to_item = {}  # Maps queue positions to the track items that occupy that position
        self._max_queue_index = 0
        self._empty_queue = None
        self._colour_scheme = colour_scheme

        # Overwrite the play function to one based on queue position
        self.play_track_function = self._mixer_controller.go_to_pos

    def _get_current_track_pos(self):
        """Return the position of the current track in the queue."""
        return self._mixer_controller.pos_in_queue

    def _get_widget_ids(self, tracks):
        """Return the `widget_id`s corresponding to the tracks.

        This overwrites `TracksDisplay.get_widget_ids()`, to use
        the queue position of a track as it's `widget_id`.
        """
        start = 0
        end = len(tracks)
        widget_ids = np.arange(start, end, step=1)
        return widget_ids

    def _get_tracks(self):
        """
        Return the list of tracks in the current queue.

        Overwrites `TracksDisplay._get_tracks()` to get the
        tracklist from the `MixerController` queue.
        """
        tracks = self._mixer_controller.active_queue
        self._max_queue_index = len(tracks) - 1
        return tracks

    def _on_play_press(self, track_item):
        """
        Call `play_track_function`.

        Overwrites `TracksDisplay.on_play_press()` to play
        based on queue position instead of `track_id`.
        """
        queue_pos = self._get_item_pos(track_item)
        self.play_track_function(queue_pos)

    def _get_item_pos(self, item):
        """Return the position of the item in the queue."""
        return item.grid_info()['row']

    def _create_buttons(self):
        """Create the additional queue display buttons for each track."""
        for track_item in self.all_track_widgets:
            # Get the position of the track in the queue
            track_pos = self._get_item_pos(track_item)
            self._pos_to_item[track_pos] = track_item

            self._create_move_buttons(track_item)
            self._create_remove_button(track_item)

    def _create_remove_button(self, track_item):
        """Create the remove button."""
        remove_button = tk.Button(track_item,
                                  text="❌",
                                  command=lambda t=track_item: self._remove_track_function(t),
                                  bg=self._colour_scheme["dark"],
                                  fg=self._colour_scheme["chili_red"],
                                  relief="flat",
                                  font=("Arial", 18))
        remove_button.grid(row=0, column=6,
                           rowspan=2, padx=20)

        track_item.track_widgets.append(remove_button)

    def _remove_track_function(self, track_item):
        """Remove a track from the queue and the display."""
        pos = self._get_item_pos(track_item)
        # remove track from the queue
        self._mixer_controller.remove_from_queue(pos)

        # destroy the widget (and remove highlight reference if necessary)
        widget = self._pos_to_item[pos]
        if widget is self.highlighted_track:
            self.highlighted_track = None
        widget.destroy()
        self._pos_to_item.pop(pos)
        # update the rest of the positions
        for position in range(pos + 1, len(self._pos_to_item)+1):
            item = self._pos_to_item[position]
            new_pos = position - 1
            # Move into the new position in the dictionary
            self._pos_to_item[new_pos] = item

            # update the widget
            item.track_number_widget.config(text=f"{new_pos+1}")
            item.grid_configure(row=new_pos)
            if position == len(self._pos_to_item)-1:
                self._pos_to_item.pop(position)  # remove the duplicate

    def _create_move_buttons(self, track_item):
        """Create the buttons to change the position of the track"""
        # Add buttons to the track items
        move_up_button = tk.Button(track_item, text="⬆️",
                                   command=lambda t=track_item: self._move_up(t),
                                   width=4, bg=self._colour_scheme["dark"], fg=self._colour_scheme["yellow"])
        move_up_button.grid(row=0, column=0)
        move_down_button = tk.Button(track_item, text="⬇️",
                                     command=lambda t=track_item: self._move_down(t),
                                     width=4, bg=self._colour_scheme["dark"], fg=self._colour_scheme["yellow"])
        move_down_button.grid(row=1, column=0)

        track_item.track_widgets.extend([move_down_button, move_up_button])

    def _move_up(self, track_item):
        """Move the track up in the queue."""
        track_pos = self._get_item_pos(track_item)
        old_index = track_pos
        new_index = old_index - 1
        if new_index < 0:
            new_index = 0

        if old_index != new_index:
            self._swap_items(old_index, new_index)

    def _move_down(self, track_item):
        """Move the track down in the queue."""
        track_pos = self._get_item_pos(track_item)
        old_index = track_pos
        new_index = old_index + 1
        if new_index >= self._max_queue_index:
            new_index = self._max_queue_index

        if old_index != new_index:
            self._swap_items(old_index, new_index)

    def _swap_items(self, old_index, new_index):
        """Swap the positions of the tracks at these positions in the queue."""
        moved_item = self._pos_to_item[old_index]
        swapped_item = self._pos_to_item[new_index]

        # Swap item positions in the dictionaries
        self._pos_to_item[new_index] = moved_item
        self._pos_to_item[old_index] = swapped_item

        # Swap the widgets' rows and update their labels
        old_row = moved_item.grid_info()['row']
        new_row = swapped_item.grid_info()['row']
        moved_item.grid_configure(row=new_row)
        swapped_item.grid_configure(row=old_row)
        moved_item.track_number_widget.config(text=new_index + 1)
        swapped_item.track_number_widget.config(text=old_index + 1)

        # Update the mixer queue
        self._mixer_controller.reorder_queue(old_index, new_index)

    def _empty_tracklist(self):
        """
        Display the screen shown when the queue is empty.

        Overwrites `TracksDisplay.empty_tracklist()`.
        """
        self._empty_queue = tk.Label(
            self.display_frame,
            text="You are currently listening to: Silence",
            bg=self._colour_scheme["grey"],
            fg=self._colour_scheme["battleship"],
            font=("Arial", 20),
        )
        self._empty_queue.grid(row=0, column=0, sticky="news")

    def update_highlighted_track(self, track_id):
        """Update the highlighted track."""
        pos = self._get_current_track_pos()  # widget_id of track that's currently playing
        if self.highlighted_track is not None:
            self.highlighted_track.remove_highlight()

        if self._pos_to_item and pos in self._pos_to_item:
            item = self._pos_to_item[pos]
            item.add_highlight()
            self.highlighted_track = item

    def clear_display(self):
        """
        Destroy all the displayed widgets.

        Overwrites `TracksDisplay.clear_display()`.
        """
        for pos in self._pos_to_item:
            self._pos_to_item[pos].destroy()

        self._pos_to_item = {}
        self.all_track_widgets = []

        if self._empty_queue:
            self._empty_queue.destroy()
            self._empty_queue = None

        self.highlighted_track = None

    def display_queue(self):
        """Create and display the queue display."""
        # Modify the start column because move up/down buttons will go in column 0
        self._start_column = 1
        super().display_tracklist()

        self._create_buttons()

        self.update_highlighted_track(None)
