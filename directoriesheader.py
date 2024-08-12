import tkinter as tk
from tkinter import filedialog

from listheader import ListHeader
from scandirectory import DirectoryScan

from root import colour_scheme


class DirectoriesHeader(ListHeader):
    """Class for the header of the directory display."""

    def __init__(self, parent, directory_scan: DirectoryScan):
        """
        Initialise a `DirectoriesHeader` instance.

        Parameters
        ----------
        parent : tkinter widget
            The parent widget containing this frame.
        directory_scan : DirectoryScan
            The instance of `DirectoryScan`.
        """
        super().__init__(parent, list_title="Add Music")
        self._directory_scan = directory_scan
        self._colour_scheme = colour_scheme

        instruction_label = tk.Label(self,
                                     text="Select a folder to add its music to your collection.",
                                     bg=self._colour_scheme["grey"],
                                     fg="white",
                                     font=("Arial", 14))
        instruction_label.grid(row=1, column=0, padx=10)

        add_button = tk.Button(self,
                               text="Add Music",
                               bg=self._colour_scheme["yellow"],
                               relief="flat",
                               font=("Arial", 14),
                               command=self._add_directory)
        add_button.grid(row=2, column=0, sticky="w", padx=10)

    def _add_directory(self):
        """Add a new directory to the list."""
        directory = filedialog.askdirectory()
        self._directory_scan.add_directory(directory)
