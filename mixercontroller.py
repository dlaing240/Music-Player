import random
import pygame.mixer as mixer
import pygame

from musicdatabase import MusicDatabase
from tracklist import TrackList
from root import Root


class MixerController:
    """
    Class to provide music player functionality and interactions with the Pygame.mixer module
    """
    def __init__(self, music_database: MusicDatabase, track_list: TrackList, root: Root):
        pygame.init()
        mixer.init(frequency=44100, size=-16, channels=2, buffer=2048)  # Initialises pygame mixer
        self.MUSIC_END_EVENT = pygame.USEREVENT + 1
        mixer.music.set_endevent(self.MUSIC_END_EVENT)

        self.music_database = music_database
        self.track_list = track_list
        self.track_list.tracklist_updated_observers.append(self)  # Mixer observes the tracklist for updates
        self.root = root

        self.track_queue = []
        self.pos_in_queue = 0  # Index of the current track in the track_queue
        self.current_track_duration = 0  # Length in seconds of the current track.
        self.current_track_id = None

        self.tracklist_changed = False
        self.repeat_setting_val = 0  # 0 = off, 1 = repeat, 2 = loop
        self.repeat_on = False
        self.loop_song_on = False
        self.shuffle_on = False
        self.current_volume = self.get_volume()

        self.new_track_observers = []  # Other objects can add themselves to the mixer controller when they want to detect song changes.
        self.now_playing_observers = []

        self._check_events()  # Starts the loop checking for the event that a song has finished.

    def _check_events(self):
        events = pygame.event.get()

        for event in events:
            if event.type == self.MUSIC_END_EVENT:
                self.song_end_procedure()
                break

        self.root.after(100, self._check_events)

    def received_tracklist_updated_signal(self):
        """
        Stores the knowledge that the tracklist has been changed in the tracklist_changed variable
        """
        self.tracklist_changed = True

    def update_queue(self):
        """
        Updates the music queue to the currently displayed tracklist, shuffling if shuffle mode is on
        """
        self.track_queue = self.track_list.get_tracklist()
        if self.shuffle_on:
            self.shuffle_queue()

        print("Queue updated. Current queue is: ", self.track_queue)
        self.tracklist_changed = False  # The queue has been changed to match the current tracklist.

    def load_next_song(self):
        """
        Loads the next song in the queue, so that it plays automatically when the current song finishes
        """
        if self.loop_song_on:
            print("Current song will repeat")
            self.queue_track(self.current_track_id)
            return

        if self.pos_in_queue + 1 < len(self.track_queue):
            print("Next song in queue is loaded")
            next_track_id = self.track_queue[self.pos_in_queue + 1]
            self.queue_track(next_track_id)
        elif self.repeat_on:
            print("Repeat is on. Playback will continue at the beginning of the queue next song")
            next_track_id = self.track_queue[0]  # Go back to the beginning of the queue
            self.queue_track(next_track_id)
        else:
            print("Repeat is OFF Playback will end at the end of the current song.")

    def update_current_track(self):
        """
        Updates information on the current track
        """
        print("updating info on current track")

        self._update_current_track_id()
        print("Current track has ID: ", self.current_track_id)

        self._update_current_track_duration()
        print("Current track has duration: ", self.current_track_duration)

    def _update_current_track_id(self):
        self.current_track_id = self.track_queue[self.pos_in_queue]

    def _update_current_track_duration(self):
        self.current_track_duration = self.music_database.get_duration(self.current_track_id)

    def received_play_track_signal(self, track_id):  # Signal that is received from the track list component to play a song.
        """
        Method to respond to the user's request to play a track
        """
        print("play_track_signal received by Mixer Controller")
        # Check whether the user is viewing a different tracklist than the current song queue
        if self.tracklist_changed:
            self.update_queue()

        self.pos_in_queue = self.track_queue.index(track_id)
        self.play_track(track_id)

        print("Playing track with track_id: ", track_id)
        print("Current music Queue is: ", self.track_queue)
        print("Current track has index", self.pos_in_queue, "in the queue.")

    def play_track(self, track_id):  # Starts playing the track with the given ID
        """
        Method to start playing a track with the given track_id
        """
        file_path = self.music_database.get_path(track_id)
        mixer.music.load(file_path)
        mixer.music.play()
        self.update_current_track()
        self.send_new_track_signal(self.current_track_id)
        self.load_next_song()

    def song_end_procedure(self):  # Procedure carried out every time a song ends
        """
        Method implementing the procedure that takes place when a song ends
        """
        print("Song has ended")

        if not self.loop_song_on:
            # Update the position in the queue
            if self.pos_in_queue < len(self.track_queue) - 1:
                self.pos_in_queue += 1
            elif self.repeat_on:
                self.pos_in_queue = 0
            else:
                return

        self.update_current_track()
        self.send_new_track_signal(self.current_track_id)  # Signals to other components that a new song is playing
        self.load_next_song()

    def stop(self):
        """
        Stops music playback
        """
        print("Stopping music playback")
        mixer.music.stop()

    def pause(self):
        """
        Pauses the current song
        """
        print("Pause")
        mixer.music.pause()

    def resume(self):
        """
        Unpause the current song
        """
        print("Resume")
        mixer.music.unpause()

    def skip(self):
        """
        Skip to the next song in the queue
        """
        self.pos_in_queue += 1
        if self.pos_in_queue >= len(self.track_queue):
            self.pos_in_queue = 0

        next_track_id = self.track_queue[self.pos_in_queue]
        self.play_track(next_track_id)
        self.send_new_track_signal(next_track_id)

    def prev(self):
        """
        If already near the start of the current track, this goes back to the previous track, otherwise it restarts the
        current track.
        """
        # Check whether more than 5 seconds into the track, in which case restart the track
        if mixer.music.get_pos() / 1000 >= 5:
            self.play_track(self.current_track_id)
            return

        # Otherwise, we want to go to the previous track
        self.pos_in_queue -= 1
        if self.pos_in_queue < 0:
            if self.repeat_on:
                self.pos_in_queue = len(self.track_queue) - 1  # go to the end of the queue if repeat is on
            else:
                self.pos_in_queue = 0  # Otherwise just repeat the track

        self.play_track(self.track_queue[self.pos_in_queue])
        self.send_new_track_signal(self.current_track_id)

    def is_playing(self):
        """
        Return true if a track is playing and false otherwise
        """
        return mixer.music.get_busy()

    def queue_track(self, track_id):
        """
        Tells the mixer module to load the track
        """
        filepath = self.music_database.get_path(track_id)
        mixer.music.queue(filepath)
        print("Track with id: ", track_id, " will play next.")

    def send_new_track_signal(self, track_id):
        """
        Signals that a new track has started playing
        """
        print("Sending new_track signal: ", track_id)
        for observer in self.new_track_observers:
            observer.received_new_track_signal(track_id)

    def get_percent_completed(self):
        """
        Returns the progress in the current track as a percentage of the track's duration
        """
        current_time = mixer.music.get_pos() / 1000  # Gives the time in seconds
        if self.current_track_duration > 0:
            percent_completed = current_time / self.current_track_duration
        else:
            percent_completed = 0

        return percent_completed

    def go_to_time(self, percentage_time):
        """
        Starts playback at the given time into the song
        """
        start_time = percentage_time * self.current_track_duration
        mixer.music.play(start=start_time)
        self.send_now_playing_signal()

    def send_now_playing_signal(self):
        """
        Signals that music is playing
        """
        for observer in self.now_playing_observers:
            observer.received_now_playing_signal()

    def set_volume(self, volume):
        """
        Sets playback volume to the given value
        """
        mixer.music.set_volume(volume)
        self.current_volume = volume

    def get_volume(self):
        """
        Returns the current playback volume
        """
        return mixer.music.get_volume()

    def received_set_volume_signal(self, volume):
        self.set_volume(volume)

    def cycle_repeat_options(self):
        """
        Cycles through the three repeat option: off, repeat queue, and repeat song
        :return:
        """
        if self.repeat_setting_val == 0:  # If repeat was turned off
            self.repeat_setting_val = 1
            self.repeat_on = True
        elif self.repeat_setting_val == 1:  # Repeat (repeat queue) was turned on
            self.repeat_on = False
            self.repeat_setting_val = 2
            self.loop_song_on = True
        else:  # Loop song was on
            self.loop_song_on = False
            self.repeat_setting_val = 0

        self.load_next_song()  # next song to be played may have been changed when the repeat setting is changed.

        return self.repeat_setting_val

    def toggle_shuffle(self):
        """
        Toggles the shuffle setting
        """
        if not self.shuffle_on:  # Shuffle is being switched on
            self.shuffle_queue()
        else:  # shuffle is being switched off.
            self.track_queue = self.track_list.get_tracklist()

        self.pos_in_queue = self.track_queue.index(self.current_track_id)  # After toggling shuffle, the current song will be in a different position
        self.shuffle_on = not self.shuffle_on
        self.load_next_song()

        return self.shuffle_on

    def shuffle_queue(self):
        """
        Shuffles the current queue
        """
        print(self.track_queue, " - queue is being shuffled")
        random.shuffle(self.track_queue)
        print("Shuffled queue is: ", self.track_queue)


