import tkinter as tk

from tkinter import font

from root import Root
from mixercontroller import MixerController
from volumeslider import VolumeSlider
from seekbar import SeekBar
from nowplaying import NowPlayingInfo
from musicdatabase import MusicDatabase

from root import colour_scheme, BUTTON_COL, CHILI_RED, BATTLESHIP_GREY, MUNSELL

# PLAY_BAR_COL = "#210B2C"
PLAY_BAR_COL = colour_scheme["dark"]


class PlayBarFrame(tk.Frame):
    """
    Class to provide the play bar frame
    """
    def __init__(self, parent: Root, mixer_controller: MixerController, music_database: MusicDatabase):
        super().__init__()

        self.parent = parent
        self.music_database = music_database
        self.mixer_controller = mixer_controller
        self.mixer_controller.new_track_observers.append(self)
        self.mixer_controller.now_playing_observers.append(self)

        self.set_volume_observers = [mixer_controller]

        self.padding_size = self.parent.padding_size
        self.grid(row=2, column=0, columnspan=2, sticky="news", padx=self.padding_size, pady=self.padding_size)
        self.config(width=800 - self.padding_size*2, height=80 - self.padding_size*2, bg=PLAY_BAR_COL)
        self._configure_grid()

        self.emoji_font = font.Font(family="Segou UI Emoji", size=20)

        self.playing = self.mixer_controller.is_playing()

        self.active = False  # Play bar is inactive until a song is loaded for the first time

        self.main_controls_frame = tk.Frame(self, bg=PLAY_BAR_COL)
        self.main_controls_frame.grid(row=1, column=2, sticky="n")

        # create widgets
        self.play_button = self._create_play_button()
        self.repeat_button, self.shuffle_button = self._create_control_buttons()

        self.seek_bar = SeekBar(self, mixer_controller)
        self.seek_bar.grid(row=0, column=2, sticky="s")

        initial_vol = self.mixer_controller.get_volume()
        self.volume_slider = VolumeSlider(self, initial_vol, self.send_set_volume_signal)
        self.volume_slider.grid(row=0, column=3, rowspan=2, padx=20, sticky="news")

        self.now_playing_info = NowPlayingInfo(self, None, None, None)
        self.now_playing_info.grid(row=0, column=0, rowspan=2, columnspan=1, padx=5, pady=20, sticky="news")

    def _configure_grid(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)

    def _event_while_inactive(self):
        print("Event ignored: Play bar is inactive")
        return

    def received_play_track_signal(self, track_id):  # this function handles the event where a user starts playing a track via the tracklist.
        """
        Method to handle the play bar's response to playback starting
        """
        print("play_track_signal received by Play Bar")
        if not self.active:
            self.active = True

        self._music_playing()

    def received_new_track_signal(self, track_id):
        """
        Method to handle play bar response to a new track starting
        """
        print("Play bar received new track signal")
        if not self.active:
            self.active = True

        self._music_playing()
        self._update_now_playing_info(track_id)

    def _music_playing(self):
        self.playing = True
        self.play_button.config(text="⏸️")

    def _not_playing(self):
        self.playing = False
        self.play_button.config(text="▶")

    def _create_play_button(self):
        play_button = tk.Button(self.main_controls_frame, text="▶", command=self._play_pause_clicked, font=("Helvetica, 20"), height=1, width=2, fg=BUTTON_COL, bg=PLAY_BAR_COL, borderwidth=0)
        play_button.grid(row=0, column=2, sticky="n", padx=5, pady=0)
        return play_button

    def _create_control_buttons(self):
        skip_button = tk.Button(self.main_controls_frame, text="⏭️", font=self.emoji_font, command=self._skip_clicked, fg=BUTTON_COL, bg=PLAY_BAR_COL, borderwidth=0)
        skip_button.grid(row=0, column=3, sticky='w', padx=5, pady=0)

        prev_button = tk.Button(self.main_controls_frame, text="⏮️", font=self.emoji_font, command=self._prev_clicked, fg=BUTTON_COL, bg=PLAY_BAR_COL, borderwidth=0)
        prev_button.grid(row=0, column=1, sticky='e', padx=5, pady=0)

        repeat_button = tk.Button(self.main_controls_frame, text="🔁", font=("Arial", 24), command=self._cycle_repeat_options, fg=BUTTON_COL, bg=PLAY_BAR_COL, borderwidth=0)
        repeat_button.grid(row=0, column=4, padx=10, sticky='e')

        shuffle_button = tk.Button(self.main_controls_frame, text="🔀", font=self.emoji_font, command=self._toggle_shuffle, fg=BUTTON_COL, bg=PLAY_BAR_COL, borderwidth=0)
        shuffle_button.grid(row=0, column=0, padx=10, sticky='w')

        return repeat_button, shuffle_button

    def _cycle_repeat_options(self):
        """
        Cycles through the display options for the repeat button
        """
        setting = self.mixer_controller.cycle_repeat_options()  # the mixer controller handles the repeat option functionality

        if setting == 0:
            self.repeat_button.config(text="🔁", fg=BUTTON_COL)
        elif setting == 1:
            self.repeat_button.config(fg=MUNSELL)
        elif setting == 2:
            self.repeat_button.config(text="🔂")

    def _toggle_shuffle(self):
        shuffle_is_on = self.mixer_controller.toggle_shuffle()
        if shuffle_is_on:
            self.shuffle_button.config(fg=MUNSELL)
        else:
            self.shuffle_button.config(fg=BUTTON_COL)

    def _play_pause_clicked(self):
        if not self.active:
            self._event_while_inactive()
            return

        if self.playing:
            self.mixer_controller.pause()
            self._not_playing()
        else:
            self.mixer_controller.resume()
            self._music_playing()

    def _skip_clicked(self):
        if not self.active:
            self._event_while_inactive()
            return

        print("User requested to skip the current track")
        self.mixer_controller.skip()

    def _prev_clicked(self):
        if not self.active:
            self._event_while_inactive()
            return

        print("User requested to jump back")
        self.mixer_controller.prev()

    def received_now_playing_signal(self):
        """
        Updates the play bar's music playing status
        """
        if not self.active:
            self.active = True
        self._music_playing()

    def send_set_volume_signal(self, volume):
        """
        Signals that volume should be set to the given value
        """
        for observer in self.set_volume_observers:
            observer.received_set_volume_signal(volume)

    def _update_now_playing_info(self, track_id):
        track_info = self.music_database.get_track_metadata(id_list=[track_id])[track_id]
        track_name = track_info["track_name"]
        artist_id = track_info["artist"]
        artist_name = self.music_database.get_artist_name(artist_id)
        album_id = track_info["album"]
        album_title = self.music_database.get_album_title(album_id)

        self.now_playing_info.update_now_playing(
            track_title=track_name,
            artist_name=artist_name,
            album=album_title)
