import tkinter as tk

from root import colour_scheme, BUTTON_COL


class AlbumItem(tk.Frame):
    """
    Class for objects that represent albums in the display.
    """
    def __init__(self, parent, open_album_command, album_id, album_name, release_date, artist_id, artist_name):
        super().__init__(parent)

        self.open_album_command = open_album_command

        self.album_id = album_id
        self.album_name = album_name
        self.release_date = release_date
        self.artist_id = artist_id
        self.artist_name = artist_name
        self._create_widgets()
        self.configure(bg=colour_scheme["dark"])

    def _create_widgets(self):
        tk.Label(self, text=self.album_name, bg=colour_scheme["dark"], fg=colour_scheme["background"], font=("Arial", 12), anchor='w').grid(row=0, column=1, padx=10,
                                                                                                     sticky='w')
        tk.Label(self, text=self.artist_name, bg=colour_scheme["dark"], fg=colour_scheme["background"], font=("Arial", 10), anchor='w').grid(row=1, column=1, padx=10,
                                                                                                      sticky='w')
        tk.Button(self, text="Open", bg=BUTTON_COL, command=self.open_album_command).grid(row=0, column=0, rowspan=2, padx=20)


