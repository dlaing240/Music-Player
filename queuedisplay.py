import tkinter as tk
import numpy as np

from tracksdisplay import TracksDisplay

from root import colour_scheme, BATTLESHIP_GREY, BUTTON_COL, CHILI_RED


class QueueDisplay(TracksDisplay):
    def __init__(self, display_frame, display_canvas, music_database,
                 track_list, mixer_controller, play_track_function,
                 add_to_queue_function, play_next_function):
        super().__init__(display_frame, display_canvas, music_database,
                         track_list, mixer_controller, play_track_function,
                         add_to_queue_function, play_next_function)
        self.pos_to_item = {}  # Maps queue positions to the track items that occupy that position
        self.max_queue_index = 0
        self.empty_queue = None

        # Overwrite the play function to one based on queue position
        self.play_track_function = self.mixer_controller.go_to_pos

    def get_current_track_pos(self):
        """
        Returns the queue position of the current track
        """
        return self.mixer_controller.pos_in_queue

    # overwrite get_widget_ids to use position for ids.
    def get_widget_ids(self, tracks):
        """
        Returns an array of queue indices to use as widget_ids.
        """
        start = 0
        end = len(tracks)
        widget_ids = np.arange(start, end, step=1)
        return widget_ids

    # Overwrite the get_tracks method
    def get_tracks(self):
        """
        Returns the list of tracks in the current queue
        """
        tracks = self.mixer_controller.active_queue
        self.max_queue_index = len(tracks) - 1
        return tracks

    def clear_display(self):
        """
        Destroys all the displayed widgets
        """
        for pos in self.pos_to_item:
            self.pos_to_item[pos].destroy()

        self.pos_to_item = {}
        self.all_track_widgets = []

        if self.empty_queue:
            self.empty_queue.destroy()
            self.empty_queue = None

        self.highlighted_track = None

    def display_queue(self):
        """
        Creates and displays the queue display
        """
        # Modify the start column because move up/down buttons will go in column 0
        self.start_column = 1
        super().display_tracklist()

        # Call method to create widgets specific to the queue display
        self.create_buttons()

        self.update_highlighted_track(None)

    def on_play_press(self, track_item):
        """
        Method called when the track_item's play button is pressed
        """
        queue_pos = self.get_item_pos(track_item)
        self.play_track_function(queue_pos)

    def get_item_pos(self, item):
        """
        Returns the queue position of the item
        """
        return item.grid_info()['row']

    def create_buttons(self):
        """
        Creates the specific queue display buttons for each track
        """

        for track_item in self.all_track_widgets:
            # Get the position of the track in the queue
            track_pos = self.get_item_pos(track_item)
            self.pos_to_item[track_pos] = track_item

            self.create_move_buttons(track_item)
            self.create_remove_button(track_item)

    def create_remove_button(self, track_item):
        """
        Creates the button to remove this track from the queue
        """
        remove_button = tk.Button(track_item,
                                  text="❌",
                                  command=lambda t=track_item: self.remove_track_function(t),
                                  bg=colour_scheme["dark"],
                                  fg=CHILI_RED,
                                  relief="flat",
                                  font=("Arial", 18))
        remove_button.grid(row=0, column=6,
                           rowspan=2, padx=20)

        track_item.track_widgets.append(remove_button)

    def remove_track_function(self, track_item):
        """
        Removes this track from the queue and the display
        """
        pos = self.get_item_pos(track_item)
        # remove track from the queue
        self.mixer_controller.remove_from_queue(pos)

        # destroy the widget (and remove highlight reference if necessary)
        widget = self.pos_to_item[pos]
        if widget is self.highlighted_track:
            self.highlighted_track = None
        widget.destroy()
        self.pos_to_item.pop(pos)

        # update the rest of the positions
        for position in range(pos + 1, len(self.pos_to_item)):
            item = self.pos_to_item[position]
            new_pos = position - 1
            self.pos_to_item[new_pos] = item
            # update the widget
            item.track_number_widget.config(text=f"{new_pos+1}")
            item.grid_configure(row=new_pos)

    def create_move_buttons(self, track_item):
        """
        Creates the buttons to change the position of this track

        Parameters
        ----------
        track_item

        Returns
        -------

        """
        # Add buttons to the track items
        move_up_button = tk.Button(track_item, text="⬆️",
                                   command=lambda t=track_item: self.move_up(t),
                                   width=4, bg=colour_scheme["dark"], fg=BUTTON_COL)
        move_up_button.grid(row=0, column=0)
        move_down_button = tk.Button(track_item, text="⬇️",
                                     command=lambda t=track_item: self.move_down(t),
                                     width=4, bg=colour_scheme["dark"], fg=BUTTON_COL)
        move_down_button.grid(row=1, column=0)

        track_item.track_widgets.extend([move_down_button, move_up_button])

    def move_up(self, track_item):
        """
        Moves the track up in the queue

        Parameters
        ----------
        track_item

        Returns
        -------

        """
        track_pos = self.get_item_pos(track_item)
        old_index = track_pos
        new_index = old_index - 1
        if new_index < 0:
            new_index = 0

        if old_index != new_index:
            self.swap_items(old_index, new_index)

    def move_down(self, track_item):
        """
        Moves the track down in the queue

        Parameters
        ----------
        track_item

        Returns
        -------

        """
        track_pos = self.get_item_pos(track_item)
        old_index = track_pos
        new_index = old_index + 1
        if new_index >= self.max_queue_index:
            new_index = self.max_queue_index

        if old_index != new_index:
            self.swap_items(old_index, new_index)

    def swap_items(self, old_index, new_index):
        """
        Swaps the positions of the tracks at these indices

        Parameters
        ----------
        old_index
        new_index

        Returns
        -------

        """
        moved_item = self.pos_to_item[old_index]
        swapped_item = self.pos_to_item[new_index]

        # Swap item positions in the dictionaries
        self.pos_to_item[new_index] = moved_item
        self.pos_to_item[old_index] = swapped_item

        # Swap the widgets' rows and update their labels
        old_row = moved_item.grid_info()['row']
        new_row = swapped_item.grid_info()['row']
        moved_item.grid_configure(row=new_row)
        swapped_item.grid_configure(row=old_row)
        moved_item.track_number_widget.config(text=new_index + 1)
        swapped_item.track_number_widget.config(text=old_index + 1)

        # Update the mixer queue
        self.mixer_controller.reorder_queue(old_index, new_index)

    def empty_tracklist(self):
        """
        Displays the screen shown when the queue is empty
        """
        self.empty_queue = tk.Label(
            self.display_frame,
            text="You are currently listening to: Silence",
            bg=colour_scheme["grey"],
            fg=BATTLESHIP_GREY,
            font=("Arial", 20),
        )
        self.empty_queue.grid(row=0, column=0, sticky="news")

    def received_add_to_queue_signal(self, track_id):
        pass

    def update_highlighted_track(self, track_id):
        """
        Updates the highlighted track


        Parameters
        ----------
        track_id

        """
        pos = self.get_current_track_pos()  # widget_id of track that's currently playing
        if self.highlighted_track is not None:
            self.highlighted_track.remove_highlight()

        if self.pos_to_item and pos in self.pos_to_item:
            item = self.pos_to_item[pos]
            item.add_highlight()
            self.highlighted_track = item
