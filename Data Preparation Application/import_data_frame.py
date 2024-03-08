from tkinter import ttk
import tkinter as tk


class ImportDataFrame(ttk.Frame):
    def __init__(self, container, *args):
        super().__init__(container)

        self.filepath = args[0]
        # setup the grid layout manager
        # self.columnconfigure(0, weight=1)
        # self.columnconfigure(0, weight=3)

        self.__create_widgets()

    def get_filename_from_path(self, filepath):
        last_slash = filepath.rfind('/')
        filename = filepath[last_slash+1:]
        filename = filename.replace('_', ' ')
        filename = filename[:filename.rfind('.')]

        return filename

    def __create_widgets(self):
        filename = self.get_filename_from_path(self.filepath)
        label_text = f'Selected file: \n {self.filepath}\n\nDataframe name: {filename}'
        # Filepath and Dataframe Label
        filepath_lbl = ttk.Label(master=self, text=label_text, anchor='center', justify='center', font=('aerial', 14))
        filepath_lbl.grid(column=0, row=0, sticky=tk.W, padx=25, pady=5)
