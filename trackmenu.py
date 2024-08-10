import tkinter as tk
from functools import partial

from root import colour_scheme
from createplaylistdialogue import CreatePlaylistDialogue


class TrackMenu:
    def __init__(self, parent, play_next_command, add_to_queue_command,
                 add_to_playlist_command, playlists,
                 create_new_playlist_command):
        self.parent = parent
        self.play_next_command = play_next_command
        self.add_to_queue_command = add_to_queue_command
        self.add_to_playlist_command = add_to_playlist_command
        self.playlists = playlists
        self.create_new_playlist_command = create_new_playlist_command

        self.create_playlist_dialogue = CreatePlaylistDialogue(self.parent, self.create_new_playlist_command)

        self.track_menu = self.create_menus()

    def create_menus(self):
        # Create the menu and add its options
        track_menu = tk.Menu(self.parent, tearoff=0,
                             bg=colour_scheme["grey"], fg="white")
        track_menu.add_command(label="⏭️ Play Next",
                               command=self.play_next_command,
                               font=("Arial", 12))
        track_menu.add_command(label="📋 Add to Queue",
                               command=self.add_to_queue_command,
                               font=("Arial", 12))

        # Create the additional playlist menu
        playlist_menu = tk.Menu(track_menu, tearoff=0,
                                bg=colour_scheme["grey"], fg="white")
        track_menu.add_cascade(label="➕ Add to Playlist",
                               menu=playlist_menu,
                               font=("Arial", 12))
        playlist_menu.add_command(label="Create New Playlist", command=self.create_playlist_dialogue.open_dialogue)
        for playlist in self.playlists:
            add_to_playlist_command = partial(self.add_to_playlist_command,
                                              playlist[0])
            playlist_menu.add_command(label=playlist[1],
                                      command=add_to_playlist_command)
        return track_menu

    def show_menu(self, event):
        self.track_menu.post(event.x_root, event.y_root)

    def update_playlist_menu(self):
        pass

    def create_new_playlist(self):
        self.create_new_playlist_command()  # E.g., opens the create playlist menu
        self.update_playlist_menu()  # Show new playlist in the menu

