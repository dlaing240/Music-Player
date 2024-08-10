import tkinter as tk
from functools import partial

from trackmenu import TrackMenu
from root import BUTTON_COL, colour_scheme, EMERALD, BATTLESHIP_GREY, MUNSELL

TRACK_LIST_COL = colour_scheme["dark"]
TEXT_COL = colour_scheme["background"]


class TrackItem(tk.Frame):
    """
    Class to provide a custom widget for displaying tracks
    """
    def __init__(self, parent, play_command, track_id, track_name,
                 artist_name, artist_id, album, album_id,
                 release_date, track_number, duration,
                 add_to_queue_command, play_next_command,
                 add_to_playlist_command, playlists,
                 create_new_playlist_command, start_column=0):
        super().__init__(parent)
        self.parent = parent
        self.play_command = play_command
        self.track_id = track_id
        self.add_to_queue_command = add_to_queue_command
        self.play_next_command = play_next_command

        self.add_to_playlist_command = add_to_playlist_command
        self.playlists = playlists  # List of (playlist_id, playlist_name) tuples
        self.create_new_playlist_command = create_new_playlist_command

        # track info
        self.track_name = track_name
        self.artist_name = artist_name
        self.artist_id = artist_id
        self.album = album
        self.album_id = album_id
        self.release_date = release_date
        self.duration = duration

        # Widget info
        self.track_number = track_number
        self.is_highlighted = False
        self.start_column = start_column
        widgets = self._create_widgets()
        self.play_track_button = widgets[0]
        self.track_widgets = [widget for widget in widgets[1:]]
        self.track_number_widget = widgets[3]
        self.menu_button = self.create_menu_button()

        self.config(bg=TRACK_LIST_COL, width=630,
                    height=30, highlightbackground=EMERALD)

    def _create_widgets(self):
        """
        Creates the track frame widgets

        Returns
        -------

        """
        number = tk.Label(self, text=f"{self.track_number}",
                          bg=TRACK_LIST_COL, fg="white",
                          font=("Arial", 10), width=3)
        number.grid(row=0, column=self.start_column, rowspan=2, padx=0)
        button = tk.Button(self, text="▶", bg=BUTTON_COL,
                           command=lambda: self.play_command(self), width=3)
        button.grid(row=0, column=self.start_column+1, rowspan=2, padx=20)
        title = tk.Label(self, text=self.track_name, bg=TRACK_LIST_COL,
                         fg="white", font=("Arial", 11), anchor='w', width=23)
        title.grid(row=0, column=self.start_column+2, padx=10, sticky='w')
        artist = tk.Label(self, text=self.artist_name, bg=TRACK_LIST_COL,
                          fg="white", font=("Arial", 10), anchor='w')
        artist.grid(row=1, column=self.start_column+2, padx=10, sticky='w')

        album_label = tk.Label(self, text=self.album,
                               bg=TRACK_LIST_COL, fg="white",
                               font=("Arial", 10), width=20, anchor="w")
        album_label.grid(row=0, column=self.start_column+3, rowspan=2, padx=10)

        duration_label = tk.Label(self, text=self.duration,
                                  bg=TRACK_LIST_COL, fg="white",
                                  font=("Arial", 8))
        duration_label.grid(row=0, column=self.start_column+5,
                            rowspan=2, padx=10)

        return button, title, artist, number, album_label, duration_label

    def create_menu_button(self):
        """
        Creates the menu button and menu options


        Returns
        -------

        """
        menu_button = tk.Button(self, text="⚫\n⚫\n⚫",
                                bg=TRACK_LIST_COL,
                                fg="white",
                                font=("Arial", 6),
                                width=4,
                                relief="flat",
                                highlightthickness=0,
                                borderwidth=0)
        menu_button.grid(row=0, column=self.start_column + 4,
                         rowspan=2, padx=10)

        track_menu = TrackMenu(self, self.play_next_command,
                               self.add_to_queue_command,
                               self.add_to_playlist_command,
                               self.playlists,
                               self.create_new_playlist_command)

        menu_button.bind("<Button-1>", track_menu.show_menu)
        return menu_button

    def add_highlight(self):
        """
        Highlights the track widget by changing the background colour
        """
        self.config(bg=MUNSELL)
        for widget in self.track_widgets:
            widget.config(bg=MUNSELL)
        self.play_track_button.config(bg=MUNSELL)
        self.menu_button.config(bg=MUNSELL)

        self.is_highlighted = True

    def remove_highlight(self):
        """
        Returns the track formatting to default
        """
        self.config(bg=TRACK_LIST_COL)
        for widget in self.track_widgets:
            widget.config(bg=TRACK_LIST_COL)
        self.play_track_button.config(bg=BUTTON_COL)
        self.menu_button.config(bg=colour_scheme["dark"])

        self.is_highlighted = False
