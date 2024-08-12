import tkinter as tk

from mixercontroller import MixerController
from root import colour_scheme
from durationformat import format_duration


class SeekBar(tk.Frame):
    """
    Class to implement an interactive progress bar.

    Methods
    -------
    received_new_track_signal(track_id):
        Reset progress bar for a new track.
    """

    def __init__(self, parent, mixer_controller: MixerController):
        """
        Initialise a `SeekBar` instance.

        Parameters
        ----------
        parent : tkinter widget
            Parent widget of this frame.
        mixer_controller : MixerController
            Instance of `MixerController`.
        """
        super().__init__(parent)
        self._mixer_controller = mixer_controller
        self._mixer_controller.new_track_observers.append(self)
        self._colour_scheme = colour_scheme

        self.configure(height=30, bg=self._colour_scheme["dark"])
        self.canvas = tk.Canvas(self,
                                width=400, height=30,
                                bg=self._colour_scheme["dark"],
                                highlightthickness=0)
        self.canvas.grid(row=0, column=0)

        self._progress_bar_width = 390
        self._progress_bar_period = 100  # Time period in ms between progress bar updates

        # Background line for the seek bar
        line = self.canvas.create_line(
            (10, 15, self._progress_bar_width, 15),
            width=5,
            fill=self._colour_scheme["battleship"]
        )
        # highlighted line which shows the current progress
        self._progress_line = self.canvas.create_line(10, 15,
                                                      10, 15,
                                                      width=5,
                                                      fill=self._colour_scheme["yellow"])
        # Create the handle which is placed on the current position in the song, and can be dragged by the user.
        self._handle = self.canvas.create_oval(0, 5, 20, 25, fill=self._colour_scheme["yellow"])

        # Label giving the current time
        self._time_label = tk.Label(self,
                                    text="0:00 / 0:00",
                                    fg="white",
                                    bg=colour_scheme["dark"])
        self._time_label.grid(row=0, column=1)

        self._displacement = 0
        self._update_progress_bar()

        self.canvas.bind("<Button-1>", self._on_click)
        self.canvas.bind("<B1-Motion>", self._on_drag)

    def _update_progress_bar(self):
        """Update the bar to show progression through a song."""
        completed = self._mixer_controller.get_percent_completed()
        xpos = completed * self._progress_bar_width + 10

        self.canvas.coords(self._handle, xpos - 10 + self._displacement,
                           5, xpos + 10 + self._displacement, 25)
        self.canvas.coords(self._progress_line, 10, 15,
                           xpos + self._displacement, 15)
        self._update_time_label(completed)
        self.after(self._progress_bar_period, self._update_progress_bar)

    def _update_time_label(self, completed):
        """Update the timer label to show the completed time."""
        duration_raw = self._mixer_controller.current_track_duration
        if self._displacement:
            percent_displacement = (
                    (self._displacement + 10) / self._progress_bar_width
            )
            time_displacement = percent_displacement * duration_raw
        else:
            time_displacement = 0

        current_time = completed * duration_raw + time_displacement
        formatted_duration = format_duration(duration_raw)
        formatted_current_time = format_duration(current_time)
        self._time_label.config(
            text=f"{formatted_current_time} / {formatted_duration}"
        )

    def _on_click(self, event):
        """Respond to a mouseclick event on the seek bar."""
        percentage_time = event.x / self._progress_bar_width
        self._mixer_controller.go_to_time(percentage_time)
        self._displacement = event.x - 10  # Progress bar starts at x=10
        self.canvas.coords(self._handle, event.x - 10, 5, event.x + 10, 25)

    def _on_drag(self, event):
        """Respond to a mouse drag event on the seek bar."""
        self._on_click(event)

    def received_new_track_signal(self, track_id):
        """Reset progress bar for a new track."""
        self._displacement = 0
