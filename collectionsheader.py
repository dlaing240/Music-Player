import tkinter as tk
from functools import partial

from root import colour_scheme, BUTTON_COL

HEADER_COL = colour_scheme["grey"]


class CollectionsHeader(tk.Frame):
    """
    Header for the display of all music tracks
    """
    def __init__(self, parent, play_all_command,
                 collection_type, collection_title, collection_id,
                 track_count, duration, subtitle=None):
        super().__init__(parent)
        self.parent = parent
        self.play_all_command = play_all_command
        self.collection_type = collection_type
        self.collection_title = collection_title
        self.collection_id = collection_id
        self.track_count = track_count
        self.duration = duration
        self.subtitle = subtitle

        self.padding_size = self.parent.padding_size
        self.config(width=640 - self.padding_size*2,
                    height=100 - self.padding_size*2, bg=HEADER_COL)
        self._grid_config()

        # unpack general widgets returned by create_general_widgets()
        (
            self.header_text,
            self.play_all_button,
            self.track_count_text,
            self.duration_text,
        ) = self.create_general_widgets()

    def _grid_config(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

    def create_general_widgets(self):
        if self.collection_type == "album":
            icon = "💿"
        elif self.collection_type == "artist":
            icon = "👤"
        else:
            icon = ""
        header_text = tk.Label(self,
                               text=f"{icon} {self.collection_title}",
                               bg=HEADER_COL, fg="White",
                               font=("Arial", 40), anchor="w")
        header_text.grid(row=0, column=0, columnspan=6, padx=5, sticky="ws")

        if self.subtitle:
            subtitle_text = tk.Label(self,
                                     text=f"👤 {self.subtitle}",
                                     bg=HEADER_COL, fg="White",
                                     font=("Arial", 14),
                                     anchor="center")
            subtitle_text.grid(row=1,
                               column=1,
                               columnspan=1,
                               padx=10,
                               sticky="w")

        play_all_button = tk.Button(self, text="Play All",
                                    bg=BUTTON_COL,
                                    fg=colour_scheme["dark"],
                                    font=("Arial", 12, "bold"),
                                    command=self.play_all_command)
        play_all_button.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        track_count_text = tk.Label(self,
                                    text=f"{self.track_count} songs",
                                    bg=HEADER_COL, fg="white",
                                    font=("Arial", 12, "bold"))
        if self.track_count == 1:
            track_count_text.config(text="1 song")
            
        track_count_text.grid(row=1, column=2, sticky="w", padx=10)

        duration_text = tk.Label(self,
                                 text=f"⏳ {self.duration}",
                                 bg=HEADER_COL, fg="white",
                                 font=("Arial", 12, "bold"))
        duration_text.grid(row=1, column=3, padx=10)

        return header_text, play_all_button, track_count_text, duration_text
