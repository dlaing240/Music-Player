import tkinter as tk

from createplaylistdialogue import CreatePlaylistDialogue
from root import colour_scheme


class CreatePlaylistButton(tk.Button):
    """A custom tkinter.Button for creating a new playlist"""

    def __init__(self, parent, create_playlist_function):
        """
        Initialise the `CreatePlaylistButton` instance.

        Parameters
        ----------
        parent : tkinter widget
            The parent widget containing this button.
        create_playlist_function : callable
            The method to create a playlist, which is passed to a
            `CreatePlaylistDialogue` instance.
        """
        super().__init__(parent)
        self.create_playlist_function = create_playlist_function
        self._colour_scheme = colour_scheme

        dialogue = CreatePlaylistDialogue(self, create_playlist_function)

        self.config(text="➕ Create Playlist",
                    command=dialogue.open_dialogue,
                    bg=self._colour_scheme["yellow"],
                    relief="flat",
                    font=("Arial", 14))
