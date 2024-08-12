import tkinter as tk
from tkinter import messagebox

from scandirectory import DirectoryScan

from root import colour_scheme


class DirectoriesDisplay:
    """
    Class to display a list of directories.

    Methods
    -------
    display():
        Display the directories list.
    clear_display():
        Destroy all widgets in the directories display.
    received_directories_updated_signal():
        Refresh the display
    """

    def __init__(self, directory_scan: DirectoryScan,
                 display_frame):
        """
        Initialise a `DirectoriesDisplay` instance.

        Parameters
        ----------
        directory_scan : DirectoryScan
            Instance of `DirectoryScan`.
        display_frame : tkinter.Frame
            The frame to place widgets upon.
        """
        self._directory_scan = directory_scan
        self._directory_labels = []
        self._display_frame = display_frame
        self._colour_scheme = colour_scheme

        self._directory_scan.directories_updated_observers.append(self)

    def display(self):
        """Display the directories list."""
        self._create_directories_list()

    def clear_display(self):
        """Destroy all widgets in the directories display."""
        for label in self._directory_labels:
            label.destroy()

        self._directory_labels = []

    def _create_directories_list(self):
        """Create labels for each directory."""
        directories = self._directory_scan.get_directories()

        if not directories:
            self._no_directories()
            return

        header_2 = tk.Label(self._display_frame,
                            text="Your music folders:",
                            bg=self._colour_scheme["grey"],
                            fg=self._colour_scheme["battleship"],
                            font=("Arial", 20)
                            )
        header_2.grid(pady=5)
        self._directory_labels.append(header_2)

        count = 1

        for directory in directories:
            directory_txt = tk.Label(
                self._display_frame,
                text=directory,
                bg=self._colour_scheme["grey"],
                fg=self._colour_scheme["battleship"],
                font=("Arial", 16)
            )
            directory_txt.grid(row=count, column=0, sticky="news", pady=5)

            remove_button = tk.Button(
                self._display_frame,
                text="❌",
                command=lambda d=directory: self._remove_directory_function(d),
                bg=self._colour_scheme["grey"],
                fg=self._colour_scheme["chili_red"],
                relief="flat",
                font=("Arial", 18))
            remove_button.grid(row=count, column=1, sticky="e")

            count += 1

            self._directory_labels.extend([directory_txt, remove_button])

    def _remove_directory_function(self, directory):
        """Remove a directory from the display and scan."""
        result = messagebox.askyesno(
            "Confirm Removal",
            "Music in this directory will be removed from your library.\nContinue?"
        )

        if result:
            self._directory_scan.remove_directory(directory)
            self._directory_scan.scan_directory()
            # refresh the display
            self.clear_display()
            self.display()
        else:
            print("Canceled")

    def _no_directories(self):
        """Create a display for an emtpy list of directories."""
        empty_label = tk.Label(self._display_frame,
                               text="Your list of folders is empty",
                               bg=self._colour_scheme["grey"],
                               fg=self._colour_scheme["battleship"],
                               font=("Arial", 14)
                               )
        empty_label.grid()
        self._directory_labels.append(empty_label)

    def received_directories_updated_signal(self):
        """Refresh the display."""
        self.clear_display()
        self.display()
