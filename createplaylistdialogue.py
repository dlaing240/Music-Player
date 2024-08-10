import tkinter as tk

from root import colour_scheme


class CreatePlaylistDialogue:
    """
    Dialogue box that opens during playlist creation
    """
    def __init__(self, parent, create_playlist_function):
        self.parent = parent
        self.create_playlist_function = create_playlist_function

    def open_dialogue(self):
        """
        Displays the dialogue informing the user to enter a name

        Returns
        -------

        """
        dialogue = tk.Toplevel(self.parent, bg=colour_scheme["grey"])
        dialogue.title("Create Playlist")

        tk.Label(dialogue,
                 text="Enter playlist name",
                 bg=colour_scheme["grey"],
                 fg="white",
                 font=("Arial", 16)).grid(row=0, column=0, padx=20, pady=10)

        name_entry = tk.Entry(dialogue)
        name_entry.grid(row=1, column=0, padx=20, pady=10)

        def submit_name():
            name = name_entry.get()
            if name:
                self.create_playlist_function(name)
                dialogue.destroy()  # Destroy the dialogue

        submit_button = tk.Button(dialogue,
                                  text="Submit",
                                  command=submit_name,
                                  bg=colour_scheme["yellow"])
        submit_button.grid(row=1, column=1, padx=20, pady=10)
