import tkinter as tk

from root import BUTTON_COL, colour_scheme, EMERALD, BATTLESHIP_GREY, MUNSELL

TRACK_LIST_COL = colour_scheme["dark"]
TEXT_COL = colour_scheme["background"]


class TrackItem(tk.Frame):
    """
    Class to provide a custom widget for displaying tracks
    """
    def __init__(self, parent, play_command, track_name, artist_name, artist_id, album, album_id, release_date, track_number, duration):
        super().__init__(parent)

        self.play_command = play_command

        # track info
        self.track_name = track_name
        self.artist_name = artist_name
        self.artist_id = artist_id
        self.album = album
        self.album_id = album_id
        self.release_date = release_date
        self.config(bg=TRACK_LIST_COL, width=630, height=30, highlightbackground=EMERALD)
        self.grid(column=0, sticky="news", pady=5, padx=10)
        self.track_number = track_number
        self.duration = duration

        widgets = self._create_widgets()
        self.play_track_button = widgets[0]
        self.track_widgets = widgets[1:]

    def _create_widgets(self):
        number = tk.Label(self, text=f"{self.track_number}", bg=TRACK_LIST_COL, fg="white", font=("Arial", 10), width=3)
        number.grid(row=0, column=0, rowspan=2, padx=0)
        button = tk.Button(self, text="▶", bg=BUTTON_COL, command=self.play_command, width=3)
        button.grid(row=0, column=1, rowspan=2, padx=20)
        title = tk.Label(self, text=self.track_name, bg=TRACK_LIST_COL, fg="white", font=("Arial", 11), anchor='w', width=23)
        title.grid(row=0, column=2, padx=10, sticky='w')
        artist = tk.Label(self, text=self.artist_name, bg=TRACK_LIST_COL, fg="white", font=("Arial", 10), anchor='w')
        artist.grid(row=1, column=2, padx=10, sticky='w')

        album_label = tk.Label(self, text=self.album, bg=TRACK_LIST_COL, fg="white", font=("Arial", 10), width=20, anchor="w")
        album_label.grid(row=0, column=3, rowspan=2, padx=10)

        duration_label = tk.Label(self, text=self.duration, bg=TRACK_LIST_COL, fg="white", font=("Arial", 8))
        duration_label.grid(row=0, column=4, rowspan=2, padx=10)

        play_next_button = tk.Button(self, text="⏭️", bg=TRACK_LIST_COL, fg="white", relief="flat")
        play_next_button.grid(row=0, column=5, rowspan=2)

        add_to_queue_button = tk.Button(self, text="📋", bg=TRACK_LIST_COL, fg="white", relief="flat", font=("Arial", 14))
        add_to_queue_button.grid(row=0, column=6, rowspan=2)

        add_to_playlist_button = tk.Button(self, text="➕", bg=TRACK_LIST_COL, fg="white", relief="flat",
                                        )
        add_to_playlist_button.grid(row=0, column=7, rowspan=2)

        return button, title, artist, number, album_label, duration_label, add_to_queue_button, add_to_playlist_button, play_next_button

    def add_highlight(self):
        """
        Highlights the track widget by changing the background colour
        """
        self.config(bg=MUNSELL)
        for widget in self.track_widgets:
            widget.config(bg=MUNSELL)
        self.play_track_button.config(bg=MUNSELL)

    def remove_highlight(self):
        """
        Returns the track formatting to default
        """
        self.config(bg=TRACK_LIST_COL)
        for widget in self.track_widgets:
            widget.config(bg=TRACK_LIST_COL)
        self.play_track_button.config(bg=BUTTON_COL)

