import tkinter as tk

from root import colour_scheme


class VolumeSlider(tk.Frame):
    """Class for a volume slider."""

    def __init__(self, parent, initial_vol, set_vol_command):
        """
        Initialise a `VolumeSlider` instance.

        Parameters
        ----------
        parent : tkinter widget
            Parent of this frame.
        initial_vol : int
            The initial volume.
        set_vol_command : callable
            Method to set the volume to a certain value.
        """
        super().__init__(parent)

        self.set_volume_command = set_vol_command
        self._colour_scheme = colour_scheme

        self.volume_icon = tk.Label(self, text="🔊", font=("Arial", 28),
                                    fg=self._colour_scheme["yellow"], bg=self._colour_scheme["dark"], width=1)
        self.volume_icon.grid(row=0, column=0, padx=10, sticky="e")

        self.slider = tk.Scale(
            self,
            from_=0,
            to=100,
            orient="horizontal",
            fg=self._colour_scheme["yellow"],
            bg=self._colour_scheme["dark"],
            highlightthickness=0,
            troughcolor=self._colour_scheme["battleship"],
            length=100,
            activebackground=self._colour_scheme["yellow"],
            width=10,
            command=self._on_set_volume
        )

        self.slider.grid(row=0, column=1, pady=30, sticky="ew")
        self.slider.set(initial_vol * 100)
        self._grid_config()
        self.config(bg=self._colour_scheme["dark"])

    def _grid_config(self):
        """Configure the grid to expand."""
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def _on_set_volume(self, volume):
        """Set the volume to the given value."""
        self._update_icon(int(volume))
        # convert volume to a value between 0 and 1 for the mixer.
        self.set_volume_command(int(volume)/100)

    def _update_icon(self, volume):
        """Update the volume icon to correspond to the volume level."""
        if volume >= 67:
            self.volume_icon.config(text="🔊")
        elif volume >= 33:
            self.volume_icon.config(text="🔉")
        elif volume > 0:
            self.volume_icon.config(text="🔈")
        else:
            self.volume_icon.config(text="🔇")
