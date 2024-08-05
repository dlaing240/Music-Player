import tkinter as tk

from root import BUTTON_COL, BATTLESHIP_GREY, colour_scheme


PLAY_BAR_COL = colour_scheme["dark"]


class VolumeSlider(tk.Frame):
    """
    Custom volume slider widget
    """
    def __init__(self, parent, initial_vol, set_vol_command):
        super().__init__(parent)

        self.set_volume_command = set_vol_command

        self.volume_icon = tk.Label(self, text="🔊", font=("Arial", 28),
                                    fg=BUTTON_COL, bg=PLAY_BAR_COL, width=1)
        self.volume_icon.grid(row=0, column=0, padx=10, sticky="e")

        self.slider = tk.Scale(
            self,
            from_=0,
            to=100,
            orient="horizontal",
            fg=BUTTON_COL,
            bg=PLAY_BAR_COL,
            highlightthickness=0,
            troughcolor=BATTLESHIP_GREY,
            length=100,
            activebackground=BUTTON_COL,
            width=10,
            command=self._on_set_volume
        )

        self.slider.grid(row=0, column=1, pady=30, sticky="ew")
        self.slider.set(initial_vol * 100)
        self._grid_config()
        self.config(bg=PLAY_BAR_COL)

    def _grid_config(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def _on_set_volume(self, volume):
        self._update_icon(int(volume))
        # convert volume to a value between 0 and 1
        self.set_volume_command(int(volume)/100)

    def _update_icon(self, volume):
        """
        Updates the volume icon to correspond to the volume level
        """
        if volume >= 67:
            self.volume_icon.config(text="🔊")
        elif volume >= 33:
            self.volume_icon.config(text="🔉")
        elif volume > 0:
            self.volume_icon.config(text="🔈")
        else:
            self.volume_icon.config(text="🔇")
