import tkinter as tk
from functools import partial

from tracksdisplay import TracksDisplay
from root import colour_scheme


class PlaylistDisplay(TracksDisplay):
    """
    Class to display the tracks in a playlist.

    Methods
    -------
    display_collection(collection_id):
        Display the playlist corresponding to the given id.
    display_tracklist():
        Display the tracklist. Overrides `TracksDisplay.display_tracklist()`.
    """

    def __init__(self, display_frame, display_canvas, music_database,
                 track_list, mixer_controller, play_track_function,
                 add_to_queue_function, play_next_function):
        """
        Initialise a `PlaylistDisplay` instance.

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
        self._remove_from_playlist_command = self._music_db.remove_from_playlist
        self._colour_scheme = colour_scheme
        self._playlist_id = None
        self._remove_buttons = {}
        self._pos_to_item = {}
        self._start_column = 1

    def _get_tracks(self):
        """
        Return a list of the tracks in the playlist.

        This method overwrites the base class' method to retrieve
        a playlist tracklist.
        """
        return self._music_db.get_playlist_tracks(self._playlist_id)

    def _create_remove_buttons(self, track_id, track_item):
        """Create the remove buttons."""
        remove_track_command = partial(self._remove_from_playlist,
                                       track_id, self._playlist_id)

        remove_button = tk.Button(track_item,
                                  text="❌",
                                  command=remove_track_command,
                                  bg=self._colour_scheme["dark"],
                                  fg=self._colour_scheme["chili_red"],
                                  relief="flat",
                                  font=("Arial", 18))
        remove_button.grid(row=0, column=6,
                           rowspan=2, padx=20)

        track_item.track_widgets.append(remove_button)

        if track_id == self.highlighted_track:
            remove_button.config(bg=self._colour_scheme["munsell"])

        self._remove_buttons[track_id] = remove_button

    def _remove_from_playlist(self, track_id, collection_id):
        """Remove a track from the playlist."""
        # remove button and widget:
        track_widget = self.widgets_dict[track_id]
        track_widget.destroy()
        self.widgets_dict.pop(track_id)

        self._remove_buttons[track_id].destroy()
        self._remove_buttons.pop(track_id)

        # Call the remove from playlist command
        self._remove_from_playlist_command(track_id, collection_id)

    def _create_move_buttons(self, track_id, track_item):
        """Create the move buttons."""
        # Add buttons to the track items
        move_up_button = tk.Button(track_item, text="⬆️",
                                   command=lambda t=(track_id, track_item): self._move_up(t),
                                   width=4, bg=self._colour_scheme["dark"], fg=self._colour_scheme["yellow"])
        move_up_button.grid(row=0, column=0)
        move_down_button = tk.Button(track_item, text="⬇️",
                                     command=lambda t=(track_id, track_item): self._move_down(t),
                                     width=4, bg=self._colour_scheme["dark"], fg=self._colour_scheme["yellow"])
        move_down_button.grid(row=1, column=0)

        track_item.track_widgets.extend([move_down_button, move_up_button])

    def _move_up(self, track):
        """Move the track up one place in the playlist."""
        track_id = track[0]
        track_pos = self._music_db.get_track_pos(self._playlist_id, track_id)
        old_index = track_pos
        new_index = old_index - 1
        min_pos = self._music_db.get_min_pos(self._playlist_id)
        if new_index < min_pos:
            new_index = min_pos

        if old_index != new_index:
            self._swap_items(track[1], old_index, new_index)

    def _move_down(self, track):
        """Move the track down one place in the playlist."""

        track_id = track[0]
        track_pos = self._music_db.get_track_pos(self._playlist_id, track_id)
        old_index = track_pos
        new_index = old_index + 1
        max_pos = self._music_db.get_max_pos(self._playlist_id)
        if new_index > max_pos:
            new_index = max_pos

        if old_index != new_index:
            self._swap_items(track[1], old_index, new_index)

    def _swap_items(self, track_item, pos_1, pos_2):
        """Swap the positions of the tracks at these positions in the playlist."""
        # Update the database
        self._music_db.swap_positions(self._playlist_id, pos_1, pos_2)

        # update widgets
        item_1 = track_item
        row_1 = item_1.grid_info()['row']
        # Find the other item
        if pos_2 > pos_1:  # Moving down
            row_2 = row_1 + 1
        else:  # Moving up
            row_2 = row_1 - 1
        item_2 = self._pos_to_item[row_2]
        item_1.grid_configure(row=row_2)
        item_1.track_number_widget.config(text=row_2+1)
        item_2.grid_configure(row=row_1)
        item_2.track_number_widget.config(text=row_1+1)
        self._pos_to_item[row_1] = item_2
        self._pos_to_item[row_2] = item_1

    def display_collection(self, collection_id):
        """Display the playlist corresponding to the given id."""
        self._playlist_id = collection_id
        self.display_tracklist()

    def display_tracklist(self):
        """
        Display the tracklist.

        Overrides `TracksDisplay.display_tracklist()` to include the
        creation of remove buttons and move buttons.
        """
        super().display_tracklist()

        pos = 0
        for track_id in self.widgets_dict:
            track_item = self.widgets_dict[track_id]
            track_item.grid_configure(row=pos)
            self._pos_to_item[pos] = track_item
            pos += 1
            self._create_remove_buttons(track_id, track_item)
            self._create_move_buttons(track_id, track_item)
