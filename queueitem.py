import tkinter as tk


from trackitem import TrackItem


from root import colour_scheme, BUTTON_COL

TRACK_LIST_COL = colour_scheme["dark"]


class QueueItem(TrackItem):
    def __init__(self, parent, play_command, track_name, artist_name,
                 artist_id, album, album_id, release_date, track_number,
                 duration, queue_index, reorder_queue_function, track_id,
                 queue_max, add_to_queue_command):
        super().__init__(parent, play_command, track_name,
                         artist_name, artist_id, album,
                         album_id, release_date, track_number,
                         duration, add_to_queue_command, start_column=1)

        self.queue_index = queue_index
        self.queue_max = queue_max
        self.reorder_queue_function = reorder_queue_function
        self.track_id = track_id

        self.track_number_widget = self.track_widgets[2]

        move_up_button = tk.Button(self, text="⬆️", command=self.move_up,
                                   width=4, bg=TRACK_LIST_COL, fg=BUTTON_COL)
        move_up_button.grid(row=0, column=0)
        move_down_button = tk.Button(self, text="⬇️", command=self.move_down,
                                     width=4, bg=TRACK_LIST_COL, fg=BUTTON_COL)
        move_down_button.grid(row=1, column=0)

    def move_up(self):
        old_index = self.queue_index
        self.queue_index -= 1
        if self.queue_index < 0:
            self.queue_index = 0

        self.update_track_number()
        self.reorder_queue_function(old_index, self.queue_index, self.track_id)

    def move_down(self):
        old_index = self.queue_index
        self.queue_index += 1
        if self.queue_index > self.queue_max:
            self.queue_index = self.queue_max

        self.update_track_number()
        self.reorder_queue_function(old_index, self.queue_index, self.track_id)

    def update_track_number(self):
        track_number = self.queue_index + 1
        self.track_number_widget.config(text=track_number)
