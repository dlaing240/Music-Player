import tkinter as tk
from functools import partial

from tracksdisplay import TracksDisplay
from root import colour_scheme, CHILI_RED, BUTTON_COL, MUNSELL


class PlaylistDisplay(TracksDisplay):
    def __init__(self, display_frame, display_canvas, music_database,
                 track_list, mixer_controller, play_track_function,
                 add_to_queue_function, play_next_function):
        super().__init__(display_frame, display_canvas, music_database,
                         track_list, mixer_controller, play_track_function,
                         add_to_queue_function, play_next_function)
        self.remove_from_playlist_command = self.music_db.remove_from_playlist
        self.playlist_id = None
        self.remove_buttons = {}
        self.pos_to_item = {}
        self.start_column = 1

    def display_collection(self, collection_id):
        self.playlist_id = collection_id
        self.display_tracklist()

    def display_tracklist(self):
        super().display_tracklist()

        pos = 0
        for track_id in self.widgets_dict:
            track_item = self.widgets_dict[track_id]
            track_item.grid_configure(row=pos)
            self.pos_to_item[pos] = track_item
            pos += 1
            self.create_remove_buttons(track_id, track_item)
            self.create_move_buttons(track_id, track_item)

    def get_tracks(self):
        return self.music_db.get_playlist_tracks(self.playlist_id)

    def create_remove_buttons(self, track_id, track_item):
        remove_track_command = partial(self.remove_from_playlist,
                                       track_id, self.playlist_id)

        remove_button = tk.Button(track_item,
                                  text="❌",
                                  command=remove_track_command,
                                  bg=colour_scheme["dark"],
                                  fg=CHILI_RED,
                                  relief="flat",
                                  font=("Arial", 18))
        remove_button.grid(row=0, column=6,
                           rowspan=2, padx=20)

        track_item.track_widgets.append(remove_button)

        if track_id == self.highlighted_track:
            remove_button.config(bg=MUNSELL)

        self.remove_buttons[track_id] = remove_button

    def remove_from_playlist(self, track_id, collection_id):
        # remove button and widget:
        track_widget = self.widgets_dict[track_id]
        track_widget.destroy()
        self.widgets_dict.pop(track_id)

        self.remove_buttons[track_id].destroy()
        self.remove_buttons.pop(track_id)

        # Call the remove from playlist command
        self.remove_from_playlist_command(track_id, collection_id)

    def create_move_buttons(self, track_id, track_item):
        """
        Creates the buttons to change the position of the track

        Parameters
        ----------
        track_id
        track_item

        Returns
        -------

        """
        # Add buttons to the track items
        move_up_button = tk.Button(track_item, text="⬆️",
                                   command=lambda t=(track_id, track_item): self.move_up(t),
                                   width=4, bg=colour_scheme["dark"], fg=BUTTON_COL)
        move_up_button.grid(row=0, column=0)
        move_down_button = tk.Button(track_item, text="⬇️",
                                     command=lambda t=(track_id, track_item): self.move_down(t),
                                     width=4, bg=colour_scheme["dark"], fg=BUTTON_COL)
        move_down_button.grid(row=1, column=0)

        track_item.track_widgets.extend([move_down_button, move_up_button])

    def move_up(self, track):
        """
        Moves the track up in the queue

        Parameters
        ----------
        track

        Returns
        -------

        """
        track_id = track[0]
        track_pos = self.music_db.get_track_pos(self.playlist_id, track_id)
        old_index = track_pos
        new_index = old_index - 1
        min_pos = self.music_db.get_min_pos(self.playlist_id)
        if new_index < min_pos:
            new_index = min_pos

        if old_index != new_index:
            self.swap_items(track[1], old_index, new_index)

    def move_down(self, track):
        """
        Moves the track down in the queue

        Parameters
        ----------
        track

        Returns
        -------

        """
        track_id = track[0]
        track_pos = self.music_db.get_track_pos(self.playlist_id, track_id)
        old_index = track_pos
        new_index = old_index + 1
        max_pos = self.music_db.get_max_pos(self.playlist_id)
        if new_index > max_pos:
            new_index = max_pos

        if old_index != new_index:
            self.swap_items(track[1], old_index, new_index)

    def swap_items(self, track_item, pos_1, pos_2):
        """
        Swaps the positions of the tracks at these indices

        Parameters
        ----------
        track_item
        pos_1
        pos_2

        Returns
        -------

        """
        # Update the mixer queue
        self.music_db.swap_positions(self.playlist_id, pos_1, pos_2)

        # update widgets
        item_1 = track_item
        row_1 = item_1.grid_info()['row']
        # Find the other item
        if pos_2 > pos_1:  # Moving down
            row_2 = row_1 + 1
        else:  # Moving up
            row_2 = row_1 - 1
        item_2 = self.pos_to_item[row_2]
        item_1.grid_configure(row=row_2)
        item_1.track_number_widget.config(text=row_2+1)
        item_2.grid_configure(row=row_1)
        item_2.track_number_widget.config(text=row_1+1)
        self.pos_to_item[row_1] = item_2
        self.pos_to_item[row_2] = item_1
