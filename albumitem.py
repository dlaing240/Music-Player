import tkinter as tk

from root import colour_scheme


class AlbumItem(tk.Frame):
    """
    Class for objects that represent albums in the display.

    It creates several widgets and places them on a tkinter frame using the grid geometry manager.

    Attributes
    ----------
    open_album_command : callable
        A function or method that is called when the open button is pressed.
    """

    def __init__(self, parent, open_album_command, album_id,
                 album_name, release_date, artist_id, artist_name):
        """
        Initialise an `AlbumItem` instance.

        Parameters
        ----------
        parent : tkinter widget
            The parent widget containing this frame.
        open_album_command : callable
            A function or method that is called when the open button is pressed.
        album_id : int
            The unique identifier for the album.
        album_name : str
            The title of the album.
        release_date : str
            The release date of the album.
        artist_id : int
            The unique identifier for the artist.
        artist_name : str
            The name of the artist.
        """
        super().__init__(parent)
        self.open_album_command = open_album_command
        self._colour_scheme = colour_scheme
        self._album_id = album_id
        self._album_name = album_name
        self._release_date = release_date
        self._artist_id = artist_id
        self._artist_name = artist_name

        self._create_widgets()
        self.configure(bg=self._colour_scheme["dark"])

    def _create_widgets(self):
        """Creates the album widgets"""
        tk.Label(
            self,
            text=self._album_name,
            bg=self._colour_scheme["dark"],
            fg=self._colour_scheme["background"],
            font=("Arial", 12),
            anchor='w'
            ).grid(
            row=0,
            column=1,
            padx=10,
            sticky='w'
        )
        tk.Label(
            self,
            text=self._artist_name,
            bg=self._colour_scheme["dark"],
            fg=self._colour_scheme["background"],
            font=("Arial", 10),
            anchor='w'
        ).grid(
            row=1,
            column=1,
            padx=10,
            sticky='w'
        )
        tk.Button(
            self,
            text="Open",
            bg=self._colour_scheme["yellow"],
            command=self.open_album_command
        ).grid(
            row=0,
            column=0,
            rowspan=2,
            padx=20)
