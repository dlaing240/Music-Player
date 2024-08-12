import tkinter as tk

from root import colour_scheme


class CollectionsHeader(tk.Frame):
    """Class for the header for music collections."""

    def __init__(self, parent, play_all_command,
                 collection_type, collection_title, collection_id,
                 track_count, duration, subtitle=None):
        """
        Initialise a `CollectionsHeader` instance.

        Parameters
        ----------
        parent : tkinter widget
            The parent widget containing this frame.
        play_all_command : callable
            The method to play all tracks in the collection.
        collection_type : {"all songs", "album", "artist", "playlist"}
            The type of music collection being displayed.
        collection_title : str
            The title of the specific collection.
        collection_id : int
            The unique identifier for the collection.
        track_count : int
            The number of tracks in this collection.
        duration : str
            The total duration of the collection. Formatted as "hh:mm:ss".
        subtitle : str, optional
            Collection subtitle, e.g., an album would have the artist's
            name as a subtitle. `None` is the default value, and will
            result in no subtitle.
        """
        super().__init__(parent)
        self._parent = parent
        self._play_all_command = play_all_command
        self._collection_type = collection_type
        self._collection_title = collection_title
        self._collection_id = collection_id
        self._track_count = track_count
        self._duration = duration
        self._subtitle = subtitle

        self._colour_scheme = colour_scheme

        self.padding_size = self._parent.padding_size
        self.config(width=640 - self.padding_size*2,
                    height=100 - self.padding_size*2, bg=self._colour_scheme["grey"])
        self._grid_config()

        self._create_general_widgets()

    def _grid_config(self):
        """Configures the expansion of the grid when the window resizes."""
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

    def _create_general_widgets(self):
        """Creates the widgets for the header."""
        if self._collection_type == "album":
            icon = "💿"
        elif self._collection_type == "artist":
            icon = "👤"
        else:
            icon = ""
        header_text = tk.Label(self,
                               text=f"{icon} {self._collection_title}",
                               bg=self._colour_scheme["grey"], fg="White",
                               font=("Arial", 40), anchor="w")
        header_text.grid(row=0, column=0, columnspan=6, padx=5, sticky="ws")

        if self._subtitle:
            subtitle_text = tk.Label(self,
                                     text=f"👤 {self._subtitle}",
                                     bg=self._colour_scheme["grey"], fg="White",
                                     font=("Arial", 14),
                                     anchor="center")
            subtitle_text.grid(row=1,
                               column=1,
                               columnspan=1,
                               padx=10,
                               sticky="w")

        play_all_button = tk.Button(self, text="Play All",
                                    bg=self._colour_scheme["yellow"],
                                    fg=self._colour_scheme["dark"],
                                    font=("Arial", 12, "bold"),
                                    command=self._play_all_command)
        play_all_button.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        track_count_text = tk.Label(self,
                                    text=f"{self._track_count} songs",
                                    bg=self._colour_scheme["grey"], fg="white",
                                    font=("Arial", 12, "bold"))
        if self._track_count == 1:
            track_count_text.config(text="1 song")
            
        track_count_text.grid(row=1, column=2, sticky="w", padx=10)

        duration_text = tk.Label(self,
                                 text=f"⏳ {self._duration}",
                                 bg=self._colour_scheme["grey"], fg="white",
                                 font=("Arial", 12, "bold"))
        duration_text.grid(row=1, column=3, padx=10)

        return header_text, play_all_button, track_count_text, duration_text
