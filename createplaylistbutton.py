import tkinter as tk

from createplaylistdialogue import CreatePlaylistDialogue
from root import colour_scheme


class CreatePlaylistButton(tk.Button):
    """
    A button for creating a new playlist
    """
    def __init__(self, parent, create_playlist_function):
        super().__init__(parent)
        self.create_playlist_function = create_playlist_function

        dialogue = CreatePlaylistDialogue(self, create_playlist_function)

        self.config(text="➕ Create Playlist",
                    command=dialogue.open_dialogue,
                    bg=colour_scheme["yellow"],
                    relief="flat",
                    font=("Arial", 14))
