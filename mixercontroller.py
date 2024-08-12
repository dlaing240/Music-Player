import random
import pygame.mixer as mixer
import pygame

from musicdatabase import MusicDatabase
from tracklist import TrackList
from root import Root


class MixerController:
    """
    Class to Interact with the pygame mixer.

    Attributes
    ----------
    active_queue : list
        List of songs in the current queue.
    pos_in_queue : int
        Current position in the queue.
    current_track_duration : float
        Duration of the current track in seconds.
    current_track_id : int
        Identifier for the currently playing track.
    new_track_observers : list
        List of observers with the method `received_new_track_signal`.
    now_playing_observers : list
        List of observers with the method `received_now_playing_signal`.

    Methods
    -------
    received_play_track_signal():
        Respond to the user's play track request.
    pause():
        Pause the current song.
    resume():
        Unpause the current song.
    skip():
        Skip to the next song in the queue.
    prev():
        Restart the track or go to the previous track.
    is_playing():
        Return true if a track is currently playing and false otherwise.
    get_percent_completed():
        Return the percentage completion of the current track's duration.
    go_to_time(percentage_time):
        Start playback at the given percentage of the track's duration.
    get_volume():
        Return the current playback volume.
    received_set_volume_signal(volume):
        Set playback volume to the given value.
    cycle_repeat_options():
        Cycle through to the next repeat option.
    toggle_shuffle():
        Toggle the shuffle setting on/off.
    reorder_queue(old_index, new_index):
        Swap the positions of the tracks at old_index and new_index.
    received_add_to_queue_signal(track_id):
        Add a track to the end of the queue.
    received_play_next_signal(track_id):
        Prepare a track to be played after the current song.
    play_all():
        Play all songs in the current tracklist.
    go_to_pos(pos):
        Start playing the track at this position in the queue.
    remove_from_queue(pos):
        Remove the track in this position from the queue.
    """

    def __init__(self, music_database: MusicDatabase,
                 track_list: TrackList, root: Root):
        """
        Initialise an `MixerController` instance.

        Parameters
        ----------
        music_database : MusicDatabase
            The `MusicDatabase` instance.
        track_list : TrackList
            The `TrackList` instance.
        root : Root
            The `Root` instance.
        """
        # Initialise pygame mixer
        pygame.init()
        mixer.init(frequency=44100, size=-16, channels=2, buffer=2048)
        self._MUSIC_END_EVENT = pygame.USEREVENT + 1
        mixer.music.set_endevent(self._MUSIC_END_EVENT)

        self._music_database = music_database
        self._track_list = track_list
        self._root = root

        self._raw_queue_list = []  # Store the tracklist when playback starts
        self.active_queue = []
        self.pos_in_queue = 0
        self.current_track_duration = 0
        self.current_track_id = None

        # self.tracklist_changed = False
        self._repeat_setting_val = 0  # 0 = off, 1 = repeat, 2 = loop
        self._repeat_on = False
        self._loop_song_on = False
        self._shuffle_on = False

        self.new_track_observers = []
        self.now_playing_observers = []

        self._check_events()

    def _check_events(self):
        """Start the loop to check for `_MUSIC_END_EVENT`."""
        events = pygame.event.get()

        for event in events:
            if event.type == self._MUSIC_END_EVENT:
                self._song_end_procedure()
                break

        self._root.after(100, self._check_events)

    def _update_queue(self):
        """Update the queue to the current tracklist"""
        self._raw_queue_list = self._track_list.get_tracklist()
        self.active_queue = self._track_list.get_tracklist()

        if self._shuffle_on:
            self._shuffle_queue()

        self._track_list.has_changed = False

    def _load_next_song(self):
        """Load the next song in the queue"""
        if self._loop_song_on:
            self._queue_track(self.current_track_id)
            return

        if self.pos_in_queue + 1 < len(self.active_queue):
            next_track_id = self.active_queue[self.pos_in_queue + 1]
            self._queue_track(next_track_id)
        elif self._repeat_on:
            # Go back to the beginning of the queue
            next_track_id = self.active_queue[0]
            self._queue_track(next_track_id)
        else:
            return

    def _update_current_track(self):
        """Update information related to the current track."""
        self.current_track_id = self.active_queue[self.pos_in_queue]
        self.current_track_duration = self._music_database.get_duration(
            self.current_track_id
        )

    def _play_track(self, track_id):
        """Play the track with the given track_id."""
        file_path = self._music_database.get_path(track_id)
        mixer.music.load(file_path)
        mixer.music.play()
        self._update_current_track()
        self._send_new_track_signal(self.current_track_id)
        self._load_next_song()

    def _song_end_procedure(self):
        """Perform the end of song procedure."""
        if not self._loop_song_on:
            # Update the position in the queue
            if self.pos_in_queue < len(self.active_queue) - 1:
                self.pos_in_queue += 1
            elif self._repeat_on:
                self.pos_in_queue = 0
            else:
                return

        self._update_current_track()
        self._send_new_track_signal(self.current_track_id)
        self._load_next_song()

    def _queue_track(self, track_id):
        """Queue a track to play after the current track."""
        filepath = self._music_database.get_path(track_id)
        mixer.music.queue(filepath)

    def _send_new_track_signal(self, track_id):
        """Signal that a new track has started playing."""
        for observer in self.new_track_observers:
            observer.received_new_track_signal(track_id)

    def _send_now_playing_signal(self):
        """Signal that music playback has started."""
        for observer in self.now_playing_observers:
            observer.received_now_playing_signal()

    def _shuffle_queue(self):
        """Shuffle the queue."""
        random.shuffle(self.active_queue)

    def _stop(self):
        """Stop music playback."""
        mixer.music.stop()

    def received_play_track_signal(self, track_id):
        """Respond to the user's play track request."""
        # Update queue if the tracklist has changed
        if self._track_list.has_changed:
            self._update_queue()

        self.pos_in_queue = self.active_queue.index(track_id)
        self._play_track(track_id)

    def pause(self):
        """Pause the current song."""
        mixer.music.pause()

    def resume(self):
        """Unpause the current song."""
        mixer.music.unpause()

    def skip(self):
        """Skip to the next song in the queue."""
        self.pos_in_queue += 1
        if self.pos_in_queue >= len(self.active_queue):
            self.pos_in_queue = 0

        next_track_id = self.active_queue[self.pos_in_queue]
        self._play_track(next_track_id)
        self._send_new_track_signal(next_track_id)

    def prev(self):
        """Restart the track or go to the previous track."""
        # Restart if more than 5 seconds into a track
        if mixer.music.get_pos() / 1000 >= 5:
            self._play_track(self.current_track_id)
            return

        # Otherwise go to the previous track
        self.pos_in_queue -= 1
        if self.pos_in_queue < 0:
            if self._repeat_on:
                # go to the end of the queue
                self.pos_in_queue = len(self.active_queue) - 1
            else:
                self.pos_in_queue = 0  # Otherwise repeat the track

        self._play_track(self.active_queue[self.pos_in_queue])
        self._send_new_track_signal(self.current_track_id)

    def is_playing(self):
        """Return true if a track is currently playing and false otherwise."""
        return mixer.music.get_busy()

    def get_percent_completed(self):
        """Return the percentage completion of the current track's duration."""
        current_time = mixer.music.get_pos() / 1000  # Gives the time in seconds
        if self.current_track_duration > 0:
            percent_completed = current_time / self.current_track_duration
        else:
            percent_completed = 0

        return percent_completed

    def go_to_time(self, percentage_time):
        """Start playback at the given percentage of the track's duration."""
        start_time = percentage_time * self.current_track_duration
        mixer.music.play(start=start_time)
        self._send_now_playing_signal()

    def get_volume(self):
        """Return the current playback volume."""
        return mixer.music.get_volume()

    def received_set_volume_signal(self, volume):
        """Set playback volume to the given value."""
        mixer.music.set_volume(volume)

    def cycle_repeat_options(self):
        """Cycle through to the next repeat option."""
        if self._repeat_setting_val == 0:  # Repeat was turned off
            self._repeat_setting_val = 1
            self._repeat_on = True
        elif self._repeat_setting_val == 1:  # Repeat was turned on
            self._repeat_on = False
            self._repeat_setting_val = 2
            self._loop_song_on = True
        else:  # Loop song was on
            self._loop_song_on = False
            self._repeat_setting_val = 0

        # This may require a different song to play next
        if self.active_queue:
            self._load_next_song()

        return self._repeat_setting_val

    def toggle_shuffle(self):
        """Toggle the shuffle setting on/off."""
        if not self._shuffle_on:  # Shuffle is being switched on
            self._shuffle_queue()
        else:  # shuffle is being switched off.
            self.active_queue = self._raw_queue_list.copy()

        if self.current_track_id and self.current_track_id in self.active_queue:
            self.pos_in_queue = self.active_queue.index(self.current_track_id)
        self._shuffle_on = not self._shuffle_on

        if self.active_queue:
            self._load_next_song()

        return self._shuffle_on

    def reorder_queue(self, old_index, new_index):
        """Swap the positions of the tracks at old_index and new_index."""
        track_id = self.active_queue.pop(old_index)
        self.active_queue.insert(new_index, track_id)
        self.pos_in_queue = self.active_queue.index(self.current_track_id)
        self._load_next_song()

    def received_add_to_queue_signal(self, track_id):
        """Add a track to the end of the queue."""
        self.active_queue.append(track_id)
        self._raw_queue_list.append(track_id)
        self._load_next_song()  # Queue has changed

    def received_play_next_signal(self, track_id):
        """Prepare a track to be played after the current song."""
        self.active_queue.insert(self.pos_in_queue+1, track_id)
        self._raw_queue_list.insert(self.pos_in_queue + 1, track_id)
        self._load_next_song()

    def play_all(self):
        """Play all songs in the current tracklist."""
        self._update_queue()  # Update the queue to match the tracklist
        # Start playing the first track in the queue
        self.pos_in_queue = 0
        self._play_track(self.active_queue[0])

    def go_to_pos(self, pos):
        """Start playing the track at this position in the queue."""
        track = self.active_queue[pos]
        self.pos_in_queue = pos
        self._play_track(track)

    def remove_from_queue(self, pos):
        """Remove the track in this position from the queue."""
        self.active_queue.pop(pos)

        if pos == self.pos_in_queue + 1:
            self._load_next_song()
        elif pos == self.pos_in_queue:
            self.pos_in_queue -= 1
            self._load_next_song()
