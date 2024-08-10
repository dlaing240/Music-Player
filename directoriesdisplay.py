import tkinter as tk
from tkinter import messagebox

from scandirectory import DirectoryScan

from root import colour_scheme, BATTLESHIP_GREY, CHILI_RED


class DirectoriesDisplay:
    def __init__(self, directory_scan: DirectoryScan,
                 display_frame):
        self.directory_scan = directory_scan
        self.directory_labels = []
        self.display_frame = display_frame

        self.directory_scan.directories_updated_observers.append(self)

    def display(self):
        self.create_directories_list()

    def clear_display(self):
        for label in self.directory_labels:
            label.destroy()

        self.directory_labels = []

    def create_directories_list(self):
        directories = self.directory_scan.get_directories()

        if not directories:
            self.no_directories()
            return

        header_2 = tk.Label(self.display_frame,
                            text="Your music folders:",
                            bg=colour_scheme["grey"],
                            fg=BATTLESHIP_GREY,
                            font=("Arial", 20)
                            )
        header_2.grid(pady=5)
        self.directory_labels.append(header_2)

        count = 1

        for directory in directories:
            directory_txt = tk.Label(
                self.display_frame,
                text=directory,
                bg=colour_scheme["grey"],
                fg=BATTLESHIP_GREY,
                font=("Arial", 16)
            )
            directory_txt.grid(row=count, column=0, sticky="news", pady=5)

            remove_button = tk.Button(
                self.display_frame,
                text="❌",
                command=lambda d=directory: self.remove_directory_function(d),
                bg=colour_scheme["grey"],
                fg=CHILI_RED,
                relief="flat",
                font=("Arial", 18))
            remove_button.grid(row=count, column=1, sticky="e")

            count += 1

            self.directory_labels.extend([directory_txt, remove_button])

    def remove_directory_function(self, directory):
        result = messagebox.askyesno(
            "Confirm Removal",
            "Music in this directory will be removed from your list.\nContinue?"
        )

        if result:
            self.directory_scan.remove_directory(directory)
            self.directory_scan.scan_directory()
            # refresh the display
            self.clear_display()
            self.display()
        else:
            print("Canceled")

    def no_directories(self):
        empty_label = tk.Label(self.display_frame,
                               text="Your list of folders is empty",
                               bg=colour_scheme["grey"],
                               fg=BATTLESHIP_GREY,
                               font=("Arial", 14)
                               )
        empty_label.grid()
        self.directory_labels.append(empty_label)

    def received_directories_updated_signal(self):
        # refresh the display
        self.clear_display()
        self.display()
