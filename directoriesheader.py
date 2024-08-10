import tkinter as tk
from tkinter import filedialog

from listheader import ListHeader
from scandirectory import DirectoryScan

from root import colour_scheme


class DirectoriesHeader(ListHeader):
    def __init__(self, parent, directory_scan: DirectoryScan):
        super().__init__(parent, list_title="Add Music")
        self.directory_scan = directory_scan

        instruction_label = tk.Label(self,
                                     text="Select a folder to add its music to your collection.",
                                     bg=colour_scheme["grey"],
                                     fg="white",
                                     font=("Arial", 14))
        instruction_label.grid(row=1, column=0, padx=10)

        add_button = tk.Button(self,
                               text="Add Music",
                               bg=colour_scheme["yellow"],
                               relief="flat",
                               font=("Arial", 14),
                               command=self.add_directory)
        add_button.grid(row=2, column=0, sticky="w", padx=10)

    def add_directory(self):
        directory = filedialog.askdirectory()
        self.directory_scan.add_directory(directory)

