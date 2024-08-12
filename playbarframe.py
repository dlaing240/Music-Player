import tkinter as tk

from tkinter import font

from root import Root
from mixercontroller import MixerController
from volumeslider import VolumeSlider
from seekbar import SeekBar
from nowplaying import NowPlayingInfo
from musicdatabase import MusicDatabase

from root import colour_scheme


class PlayBarFrame(tk.Frame):
    """
    Class to provide the play bar frame.

    Attributes
    ----------
    set_volume_observers

    Methods
    -------
    received_now_playing_signal():
        Update the play bar's music playing status.
    received_play_track_signal(track_id):
        Set playbar status to active.
    received_new_track_signal(track_id):
        Update play bar in response to a new track.
    """

    def __init__(self, parent: Root,
                 mixer_controller: MixerController,
                 music_database: MusicDatabase):
        """
        Initialise a `PlayBarFrame` instance.

        Parameters
        ----------
        parent : tkinter widget
            The parent widget of this frame.
        mixer_controller : MixerController
            Instance of `MixerController`.
        music_database : MusicDatabase
            Instance of `MusicDatabase`.
        """
        super().__init__()

        self.parent = parent
        self._music_database = music_database
        self._mixer_controller = mixer_controller
        self._mixer_controller.new_track_observers.append(self)
        self._mixer_controller.now_playing_observers.append(self)
        self._colour_scheme = colour_scheme

        self.set_volume_observers = [mixer_controller]

        self.padding_size = self.parent.padding_size
        self.grid(row=2, column=0, columnspan=2, sticky="news",
                  padx=self.padding_size, pady=self.padding_size)
        self.config(width=800 - self.padding_size*2,
                    height=80 - self.padding_size*2, bg=self._colour_scheme["dark"])
        self._configure_grid()

        self._emoji_font = font.Font(family="Segou UI Emoji", size=20)
        self._playing = self._mixer_controller.is_playing()
        # Play bar is inactive until a song is loaded for the first time
        self._active = False

        self._main_controls_frame = tk.Frame(self, bg=self._colour_scheme["dark"])
        self._main_controls_frame.grid(row=1, column=2, sticky="n")

        self._play_button = self._create_play_button()
        self._repeat_button, self.shuffle_button = self._create_control_buttons()

        self._seek_bar = SeekBar(self, mixer_controller)
        self._seek_bar.grid(row=0, column=2, sticky="s")

        initial_vol = self._mixer_controller.get_volume()
        self._volume_slider = VolumeSlider(self, initial_vol,
                                           self._send_set_volume_signal)
        self._volume_slider.grid(row=0, column=3,
                                 rowspan=2, padx=20, sticky="news")
        self._now_playing_info = NowPlayingInfo(self)
        self._now_playing_info.grid(row=0, column=0, rowspan=2, columnspan=1,
                                    padx=5, pady=20, sticky="news")

    def _configure_grid(self):
        """Configure the way the grid expands."""
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)

    def _music_playing(self):
        """Set `playing` to True."""
        self._playing = True
        self._play_button.config(text="⏸️")

    def _not_playing(self):
        """Set `playing` to False."""
        self._playing = False
        self._play_button.config(text="▶")

    def _create_play_button(self):
        """Create the play/pause button widget."""
        play_button = tk.Button(self._main_controls_frame, text="▶",
                                command=self._play_pause_clicked,
                                font=("Helvetica, 20"), height=1,
                                width=2, fg=self._colour_scheme["yellow"],
                                bg=self._colour_scheme["dark"], borderwidth=0)
        play_button.grid(row=0, column=2, sticky="n", padx=5, pady=0)
        return play_button

    def _create_control_buttons(self):
        """Create button widgets to control playback."""
        skip_button = tk.Button(self._main_controls_frame, text="⏭️",
                                font=self._emoji_font,
                                command=self._skip_clicked,
                                fg=self._colour_scheme["yellow"],
                                bg=self._colour_scheme["dark"],
                                borderwidth=0)
        skip_button.grid(row=0, column=3, sticky='w', padx=5, pady=0)

        prev_button = tk.Button(self._main_controls_frame, text="⏮️",
                                font=self._emoji_font,
                                command=self._prev_clicked,
                                fg=self._colour_scheme["yellow"], bg=self._colour_scheme["dark"],
                                borderwidth=0)
        prev_button.grid(row=0, column=1, sticky='e', padx=5, pady=0)

        repeat_button = tk.Button(self._main_controls_frame, text="🔁",
                                  font=("Arial", 24),
                                  command=self._cycle_repeat_options,
                                  fg=self._colour_scheme["yellow"], bg=self._colour_scheme["dark"],
                                  borderwidth=0)
        repeat_button.grid(row=0, column=4, padx=10, sticky='e')

        shuffle_button = tk.Button(self._main_controls_frame, text="🔀",
                                   font=self._emoji_font,
                                   command=self._toggle_shuffle,
                                   fg=self._colour_scheme["yellow"], bg=self._colour_scheme["dark"],
                                   borderwidth=0)
        shuffle_button.grid(row=0, column=0, padx=10, sticky='w')

        return repeat_button, shuffle_button

    def _cycle_repeat_options(self):
        """Cycle through the display options for the repeat button widget."""
        setting = self._mixer_controller.cycle_repeat_options()
        if setting == 0:
            self._repeat_button.config(text="🔁", fg=self._colour_scheme["yellow"])
        elif setting == 1:
            self._repeat_button.config(fg=self._colour_scheme["munsell"])
        elif setting == 2:
            self._repeat_button.config(text="🔂")

    def _toggle_shuffle(self):
        """Toggle the appearance of the shuffle button."""
        shuffle_is_on = self._mixer_controller.toggle_shuffle()
        if shuffle_is_on:
            self.shuffle_button.config(fg=self._colour_scheme["munsell"])
        else:
            self.shuffle_button.config(fg=self._colour_scheme["yellow"])

    def _play_pause_clicked(self):
        """Play or pause the music."""
        if not self._active:
            return

        if self._playing:
            self._mixer_controller.pause()
            self._not_playing()
        else:
            self._mixer_controller.resume()
            self._music_playing()

    def _skip_clicked(self):
        """Call `MixerController.skip()`."""
        if not self._active:
            return

        self._mixer_controller.skip()

    def _prev_clicked(self):
        """Call `MixerController.prev()."""
        if not self._active:
            return

        self._mixer_controller.prev()

    def _send_set_volume_signal(self, volume):
        """Signal that volume should be set to the given value."""
        for observer in self.set_volume_observers:
            observer.received_set_volume_signal(volume)

    def _update_now_playing_info(self, track_id):
        """Update the `NowPlayingInfo` instance."""
        track_info = self._music_database.get_track_metadata(
            id_list=[track_id]
        )[track_id]
        track_name = track_info["track_name"]
        artist_id = track_info["artist"]
        artist_name = self._music_database.get_artist_name(artist_id)
        album_id = track_info["album"]
        album_title = self._music_database.get_album_title(album_id)

        self._now_playing_info.update_now_playing(
            track_title=track_name,
            artist_name=artist_name,
            album=album_title)

    def received_now_playing_signal(self):
        """Update the play bar's music playing status."""
        if not self._active:
            self._active = True
        self._music_playing()

    def received_play_track_signal(self, track_id):
        """Set playbar status to active."""
        if not self._active:
            self._active = True

        self._music_playing()

    def received_new_track_signal(self, track_id):
        """Update play bar in response to a new track."""
        if not self._active:
            self._active = True

        self._music_playing()
        self._update_now_playing_info(track_id)
