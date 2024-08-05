import tkinter as tk

from mixercontroller import MixerController
from root import BATTLESHIP_GREY, colour_scheme, BUTTON_COL
from durationformat import format_duration

PLAY_BAR_COL = colour_scheme["dark"]


class SeekBar(tk.Frame):
    """
    Class to implement an interactive progress bar
    """
    def __init__(self, parent, mixer_controller: MixerController):
        super().__init__(parent)
        self.mixer_controller = mixer_controller
        self.mixer_controller.new_track_observers.append(self)

        self.configure(height=30, bg=PLAY_BAR_COL)
        self.canvas = tk.Canvas(self,
                                width=400, height=30,
                                bg=PLAY_BAR_COL,
                                highlightthickness=0)
        self.canvas.grid(row=0, column=0)

        self.progress_bar_width = 390
        self.progress_bar_period = 100  # Time period in ms between progress bar updates

        # Background line for the seek bar
        self.line = self.canvas.create_line(
            (10, 15, self.progress_bar_width, 15),
            width=5,
            fill=BATTLESHIP_GREY
        )
        # highlighted line which shows the current progress
        self.progress_line = self.canvas.create_line(10, 15,
                                                     10, 15,
                                                     width=5,
                                                     fill=BUTTON_COL)
        # Create the handle which is placed on the current position in the song, and can be dragged by the user.
        self.handle = self.canvas.create_oval(0, 5, 20, 25, fill=BUTTON_COL)

        # Label giving the current time
        self.time_label = tk.Label(self,
                                   text="0:00 / 0:00",
                                   fg="white",
                                   bg=colour_scheme["dark"])
        self.time_label.grid(row=0, column=1)

        self.displacement = 0
        self._update_progress_bar()

        self.canvas.bind("<Button-1>", self._on_click)
        self.canvas.bind("<B1-Motion>", self._on_drag)

    def _update_progress_bar(self):
        """
        Updates the bar to show progression through a song
        """
        completed = self.mixer_controller.get_percent_completed()
        xpos = completed * self.progress_bar_width + 10

        self.canvas.coords(self.handle, xpos-10 + self.displacement,
                           5, xpos+10 + self.displacement, 25)
        self.canvas.coords(self.progress_line, 10, 15,
                           xpos + self.displacement, 15)
        self._update_time_label(completed)
        self.after(self.progress_bar_period, self._update_progress_bar)

    def _update_time_label(self, completed):
        """
        Updates the label next to the progress bar which displays the timer
        """
        duration_raw = self.mixer_controller.current_track_duration
        if self.displacement:
            percent_displacement = (
                    (self.displacement + 10) / self.progress_bar_width
            )
            time_displacement = percent_displacement * duration_raw
        else:
            time_displacement = 0

        current_time = completed * duration_raw + time_displacement
        formatted_duration = format_duration(duration_raw)
        formatted_current_time = format_duration(current_time)
        self.time_label.config(
            text=f"{formatted_current_time} / {formatted_duration}"
        )

    def _on_click(self, event):
        percentage_time = event.x / self.progress_bar_width
        self.mixer_controller.go_to_time(percentage_time)
        self.displacement = event.x - 10  # Progress bar starts at x=10
        self.canvas.coords(self.handle, event.x-10, 5, event.x+10, 25)

    def _on_drag(self, event):
        self._on_click(event)

    def received_new_track_signal(self, track_id):
        """
        Resets attributes related to the progress bar when it receives a
        signal that the track changes.
        """
        self.displacement = 0
