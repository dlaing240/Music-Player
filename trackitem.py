import tkinter as tk
from functools import partial

from trackmenu import TrackMenu
from root import colour_scheme


class TrackItem(tk.Frame):
    """
    Class for a widget representing a track.

    Attributes
    ----------

    Methods
    -------

    """

    def __init__(self, parent, play_command, track_id, track_name,
                 artist_name, artist_id, album, album_id,
                 release_date, track_number, duration,
                 add_to_queue_command, play_next_command,
                 add_to_playlist_command, playlists,
                 create_new_playlist_command, start_column=0):
        """
        Initialise a `TrackItem` instance.

        Parameters
        ----------
        parent : tkinter widget
            The parent widget of this frame.
        play_command : callable
            Method to play a track.
        track_id : int
            Unique identifier for the track.
        track_name : str
            The title of the track.
        artist_name : str
            The name of the artist.
        artist_id : int
            The unique identifier for the artist.
        album : str
            The title of the album.
        album_id : int
            Identifier for the album.
        release_date : str
            The track's release date.
        track_number : int
            The position of the track in the tracklist.
        duration : str
            The duration of the track.
        add_to_queue_command : callable
            Method to add the track to the queue.
        play_next_command : callable
            Method to play the track next.
        add_to_playlist_command : callable
            Method to add the track to a playlist.
        playlists : list
            List of playlists.
        create_new_playlist_command : callable
            Method to create a new playlist.
        start_column : int
            The column number to place the first widgets on.
        """
        super().__init__(parent)
        self._parent = parent
        self._play_command = play_command
        self._add_to_queue_command = add_to_queue_command
        self._play_next_command = play_next_command
        self._add_to_playlist_command = add_to_playlist_command
        self._playlists = playlists  # List of (playlist_id, playlist_name) tuples
        self._create_new_playlist_command = create_new_playlist_command
        self._colour_scheme = colour_scheme

        # track info
        self.track_id = track_id
        self._track_name = track_name
        self._artist_name = artist_name
        self._artist_id = artist_id
        self._album = album
        self._album_id = album_id
        self._release_date = release_date
        self._duration = duration

        # Widget info
        self._track_number = track_number
        self._is_highlighted = False
        self._start_column = start_column
        widgets = self._create_widgets()
        self._play_track_button = widgets[0]
        self.track_widgets = [widget for widget in widgets[1:]]
        self.track_number_widget = widgets[3]
        self._menu_button = self._create_menu_button()

        self.config(bg=self._colour_scheme["dark"], width=630,
                    height=30, highlightbackground=self._colour_scheme["emerald"])

    def _create_widgets(self):
        """Create the track widgets."""
        number = tk.Label(self, text=f"{self._track_number}",
                          bg=self._colour_scheme["dark"], fg="white",
                          font=("Arial", 10), width=3)
        number.grid(row=0, column=self._start_column, rowspan=2, padx=0)
        button = tk.Button(self, text="▶", bg=self._colour_scheme["yellow"],
                           command=lambda: self._play_command(self), width=3)
        button.grid(row=0, column=self._start_column + 1, rowspan=2, padx=20)
        title = tk.Label(self, text=self._track_name, bg=self._colour_scheme["dark"],
                         fg="white", font=("Arial", 11), anchor='w', width=23)
        title.grid(row=0, column=self._start_column + 2, padx=10, sticky='w')
        artist = tk.Label(self, text=self._artist_name, bg=self._colour_scheme["dark"],
                          fg="white", font=("Arial", 10), anchor='w')
        artist.grid(row=1, column=self._start_column + 2, padx=10, sticky='w')

        album_label = tk.Label(self, text=self._album,
                               bg=self._colour_scheme["dark"], fg="white",
                               font=("Arial", 10), width=20, anchor="w")
        album_label.grid(row=0, column=self._start_column + 3, rowspan=2, padx=10)

        duration_label = tk.Label(self, text=self._duration,
                                  bg=self._colour_scheme["dark"], fg="white",
                                  font=("Arial", 8))
        duration_label.grid(row=0, column=self._start_column + 5,
                            rowspan=2, padx=10)

        return button, title, artist, number, album_label, duration_label

    def _create_menu_button(self):
        """Create the menu button and menu options."""
        menu_button = tk.Button(self, text="⚫\n⚫\n⚫",
                                bg=self._colour_scheme["dark"],
                                fg="white",
                                font=("Arial", 6),
                                width=4,
                                relief="flat",
                                highlightthickness=0,
                                borderwidth=0)
        menu_button.grid(row=0, column=self._start_column + 4,
                         rowspan=2, padx=10)

        track_menu = TrackMenu(self, self._play_next_command,
                               self._add_to_queue_command,
                               self._add_to_playlist_command,
                               self._playlists,
                               self._create_new_playlist_command)

        menu_button.bind("<Button-1>", track_menu.show_menu)
        return menu_button

    def add_highlight(self):
        """Highlight the track widget by changing the background colour."""
        self.config(bg=self._colour_scheme["munsell"])
        for widget in self.track_widgets:
            widget.config(bg=self._colour_scheme["munsell"])
        self._play_track_button.config(bg=self._colour_scheme["munsell"])
        self._menu_button.config(bg=self._colour_scheme["munsell"])

        self._is_highlighted = True

    def remove_highlight(self):
        """Remove the highlight."""
        self.config(bg=self._colour_scheme["dark"])
        for widget in self.track_widgets:
            widget.config(bg=self._colour_scheme["dark"])
        self._play_track_button.config(bg=self._colour_scheme["yellow"])
        self._menu_button.config(bg=self._colour_scheme["dark"])

        self._is_highlighted = False
