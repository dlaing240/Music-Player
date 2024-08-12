import tkinter as tk

from root import colour_scheme


class CreatePlaylistDialogue:
    """A dialogue box that opens during playlist creation"""

    def __init__(self, parent, create_playlist_function):
        """
        Initialise a `CreatePlaylistDialogue` instance.

        Parameters
        ----------
        parent : tkinter widget
            The parent widget of the dialogue box.
        create_playlist_function : callable
            The method to create a playlist that is called when the
            dialogue submit button is pressed.
        """
        self._parent = parent
        self._create_playlist_function = create_playlist_function
        self._colour_scheme = colour_scheme

    def open_dialogue(self):
        """Display the dialogue informing the user to enter a name"""
        dialogue = tk.Toplevel(self._parent, bg=self._colour_scheme["grey"])
        dialogue.title("Create Playlist")

        tk.Label(dialogue,
                 text="Enter playlist name",
                 bg=self._colour_scheme["grey"],
                 fg="white",
                 font=("Arial", 16)).grid(row=0, column=0, padx=20, pady=10)

        name_entry = tk.Entry(dialogue)
        name_entry.grid(row=1, column=0, padx=20, pady=10)

        def submit_name():
            name = name_entry.get()
            if name:
                self._create_playlist_function(name)
                dialogue.destroy()

        submit_button = tk.Button(dialogue,
                                  text="Submit",
                                  command=submit_name,
                                  bg=self._colour_scheme["yellow"])
        submit_button.grid(row=1, column=1, padx=20, pady=10)
