import tkinter as tk

from root import colour_scheme, BUTTON_COL


class PlaylistItem(tk.Frame):
    """
    Class for objects that represent playlists in the display.
    """
    def __init__(self, parent, open_playlist_command, playlist_id,
                 playlist_name):
        super().__init__(parent)
        self.open_playlist_command = open_playlist_command
        self.playlist_id = playlist_id
        self.playlist_name = playlist_name

        self._create_widgets()
        self.configure(bg=colour_scheme["dark"])

        self.grid_columnconfigure(1, weight=1)

    def _create_widgets(self):
        tk.Label(
            self,
            text=self.playlist_name,
            bg=colour_scheme["dark"],
            fg=colour_scheme["background"],
            font=("Arial", 12),
            anchor='w',
            height=2,
            ).grid(
            row=0,
            column=1,
            rowspan=2,
            padx=10,
            sticky='nesw'
        )
        tk.Button(
            self,
            text="Open",
            bg=BUTTON_COL,
            command=self.open_playlist_command
        ).grid(
            row=0,
            column=0,
            rowspan=2,
            padx=20)
